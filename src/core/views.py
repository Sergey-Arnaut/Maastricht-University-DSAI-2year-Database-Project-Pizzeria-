from datetime import datetime, timedelta, date

from django.contrib import messages
from django.db import transaction, connection
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import (
    Customer, Pizza, Order, Orderitem,
    Discountcode, Discountredemption, Deliveryperson
)


def menu(request):
    price_map = {p.pizza_id: p for p in Pizzapriceview.objects.all()}
    pizzas = Pizza.objects.filter(availability=True)

    items = []
    for p in pizzas:
        v = price_map.get(p.pizza_id)
        items.append({
            "id": p.pizza_id,
            "name": p.name,
            "size": p.size,
            "is_vegan": getattr(p, "is_vegan", False),
            "is_vegetarian": getattr(p, "is_vegetarian", False),
            "price": getattr(v, "price_with_vat", None) or getattr(v, "price_no_vat", None),
            "ingredients_cost": getattr(v, "ingredients_cost", None),
        })
    return render(request, "menu.html", {"items": items})

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

# ==== корзина через сессию ====
def _get_cart(request):
    """cart = {"<pizza_id>": qty, ...}"""
    return request.session.get("cart", {})

def _save_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True

def _demo_customer():
    """Для демо берём/создаём одного клиента (позже замените на auth)."""
    cust, _ = Customer.objects.get_or_create(
        email="demo@example.com",
        defaults=dict(first_name="Demo", last_name="User", postal_code="62150", date_of_birth=date(2000, 10, 1)),
    )
    return cust

def _fetch_cart_rows(cart: dict):
    """
    Возвращает список строк корзины с данными из БД:
    [{"pizza": Pizza, "qty": int, "unit": Decimal, "sum": Decimal}, ...], subtotal
    """
    if not cart:
        return [], 0
    ids = [int(k) for k in cart.keys()]
    pizzas = {p.pizza_id: p for p in Pizza.objects.filter(pizza_id__in=ids)}
    rows, subtotal = [], 0.0
    for pid, qty in cart.items():
        p = pizzas.get(int(pid))
        if not p:
            continue
        unit = float(getattr(p, "base_price", 0.0))
        summ = round(unit * int(qty), 2)
        rows.append({"pizza": p, "qty": int(qty), "unit": unit, "sum": summ})
        subtotal += summ
    return rows, round(subtotal, 2)

def _customer_total_pizzas(customer_id: int) -> int:
    """
    Считает сколько пицц клиент заказал ранее (по всем заказам с любым статусом).
    Для продакшена можно ограничить статусами 'delivered/ready/...'.
    """
    with connection.cursor() as cur:
        cur.execute("""
            SELECT COALESCE(SUM(oi.pizza_quantity), 0)
            FROM OrderItem oi
            JOIN `Order` o ON o.order_id = oi.order_id
            WHERE o.customer_id = %s
        """, [customer_id])
        row = cur.fetchone()
    return int(row[0] or 0)

def _apply_discounts(customer: Customer, rows: list, subtotal: float, discount_code_input: str):
    """
    Возвращает (total, discount_amount, applied: dict) и, если применён одноразовый код,
    объект Discountcode для записи в Order + DiscountRedemption.
    Правила:
      - LOYALTY: если клиент пересекает кратность 10 пицц, дарим ЛУЧШУЮ скидку = цена самой дешёвой пиццы в корзине.
      - BIRTHDAY: если сегодня ДР клиента — доп. скидка 10% (можно заменить на free dessert).
      - DISCOUNT CODE: одноразовый код percent/value в рамках дат.
    Скидки суммируются, но не могут опустить total ниже нуля.
    """
    applied = {}
    discount_amount_total = 0.0
    code_obj = None

    # Loyalty (каждые 10 пицц — бесплатная самая дешёвая)
    prev_count = _customer_total_pizzas(customer.customer_id)
    in_cart = sum(r["qty"] for r in rows)
    crosses = (prev_count // 10) < ((prev_count + in_cart) // 10)
    if crosses and rows:
        cheapest = min((r["unit"] for r in rows), default=0.0)
        if cheapest > 0:
            applied["loyalty_free_pizza"] = cheapest
            discount_amount_total += cheapest

    # Birthday (сегодня совпадает день/месяц)
    if customer.date_of_birth:
        dob = customer.date_of_birth
        today = date.today()
        if dob.month == today.month and dob.day == today.day:
            bday_disc = round(subtotal * 0.10, 2)  # 10%
            if bday_disc > 0:
                applied["birthday_10pct"] = bday_disc
                discount_amount_total += bday_disc

    # One-time discount code
    discount_code_input = (discount_code_input or "").strip()
    if discount_code_input:
        try:
            code = Discountcode.objects.get(discount_code=discount_code_input, is_active=True)
            today = date.today()
            if (code.valid_from and today < code.valid_from) or (code.valid_until and today > code.valid_until):
                code = None  # вне периода действия
        except Discountcode.DoesNotExist:
            code = None

        if code:
            # проверим, не погасил ли клиент уже этот код
            already = Discountredemption.objects.filter(
                discount_id=code.discount_id, customer_id=customer.customer_id
            ).exists()
            if not already:
                if code.discount_type == "percent":
                    val = round(subtotal * (code.discount_value / 100.0), 2)
                else:
                    val = float(code.discount_value)
                if val > 0:
                    applied["code_"+code.discount_code] = val
                    discount_amount_total += val
                    code_obj = code

    # Итог
    total = round(max(subtotal - discount_amount_total, 0.0), 2)
    return total, round(discount_amount_total, 2), applied, code_obj

def _assign_delivery(order_id: int, delivery_postal_code: str):
    """
    Назначает курьера по правилам:
      - delivery_postal_code совпадает
      - availability = TRUE
      - НЕ назначен на другой заказ за последние 30 минут
      - приоритет: минимальный number_of_orders, затем лучший rating (DESC)
    Возвращает delivery_person_id или None.
    """
    with connection.cursor() as cur:
        cur.execute("""
            SELECT dp.delivery_person_id
            FROM DeliveryPerson dp
            WHERE dp.availability = TRUE
              AND dp.delivery_postal_code = %s
              AND NOT EXISTS (
                    SELECT 1
                    FROM `Order` o2
                    WHERE o2.delivery_id = dp.delivery_person_id
                      AND o2.order_timestamp >= (NOW() - INTERVAL 30 MINUTE)
                      AND o2.status IN ('pending','preparing','baking','ready','out_for_delivery')
              )
            ORDER BY dp.number_of_orders ASC, dp.rating DESC
            LIMIT 1
        """, [delivery_postal_code])
        row = cur.fetchone()

    if not row:
        return None

    dp_id = int(row[0])

    # Проставим в заказ и увеличим счётчик (сделаем атомарно)
    with connection.cursor() as cur, transaction.atomic():
        cur.execute("UPDATE `Order` SET delivery_id=%s WHERE order_id=%s", [dp_id, order_id])
        cur.execute("UPDATE DeliveryPerson SET number_of_orders = number_of_orders + 1 WHERE delivery_person_id=%s", [dp_id])

    return dp_id

# -------------------------
# VIEW'хи
# -------------------------

def menu(request):
    # если ты уже делал меню с VIEW цен — оставь как было
    cart = _get_cart(request)
    # Соберём короткую витрину (без VIEW): доступные пиццы
    pizzas = Pizza.objects.filter(availability=True)[:50]
    items = [{
        "id": p.pizza_id,
        "name": p.name,
        "size": p.size,
        "price": getattr(p, "base_price", 0),
        "is_vegan": getattr(p, "is_vegan", False),
        "is_vegetarian": getattr(p, "is_vegetarian", False),
    } for p in pizzas]
    return render(request, "menu.html", {"items": items, "cart_count": sum(cart.values())})

def view_cart(request):
    rows, subtotal = _fetch_cart_rows(_get_cart(request))
    return render(request, "cart.html", {"rows": rows, "subtotal": subtotal})

@require_POST
def add_to_cart(request, pizza_id: int):
    qty = max(1, int(request.POST.get("qty", 1)))
    cart = _get_cart(request)
    cart[str(pizza_id)] = cart.get(str(pizza_id), 0) + qty
    _save_cart(request, cart)
    return redirect("view_cart")

@require_POST
def remove_from_cart(request, pizza_id: int):
    cart = _get_cart(request)
    cart.pop(str(pizza_id), None)
    _save_cart(request, cart)
    return redirect("view_cart")

@require_POST
def clear_cart(request):
    _save_cart(request, {})
    return redirect("view_cart")

@require_POST
def checkout(request):
    """
    Создаёт заказ + позиции, применяет скидки (loyalty/birthday/code),
    назначает курьера по индексу и ограничению 30 минут.
    """
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, "Корзина пуста.")
        return redirect("menu")

    customer = _demo_customer()  # TODO: заменить на реального пользователя/форму доставки
    rows, subtotal = _fetch_cart_rows(cart)
    discount_code_input = request.POST.get("discount_code", "")

    total, discount_amount, applied, code_obj = _apply_discounts(customer, rows, subtotal, discount_code_input)

    # Создаём заказ и позиции
    with transaction.atomic():
        order = Order.objects.create(
            customer_id=customer.customer_id,
            order_timestamp=datetime.now(),
            status="pending",
            total_price=total,
            delivery_postal_code=customer.postal_code or "00000",
            discount_id=(code_obj.discount_id if code_obj else None),
            discount_amount=discount_amount,
        )
        # позиции заказа
        for r in rows:
            Orderitem.objects.create(
                order_id=order.order_id,
                pizza_id=r["pizza"].pizza_id,
                pizza_quantity=r["qty"],
                item_current_price=r["unit"],
            )

        # если использован одноразовый код — запишем редемпшн (связка код-клиент-заказ)
        if code_obj:
            Discountredemption.objects.get_or_create(
                discount_id=code_obj.discount_id,
                customer_id=customer.customer_id,
                order_id=order.order_id,
            )

        # назначим доставщика
        dp_id = _assign_delivery(order.order_id, order.delivery_postal_code)

    # Очистим корзину и покажем результат
    _save_cart(request, {})
    messages.success(request, f"Заказ #{order.order_id} создан. Скидок применено на {discount_amount}€")
    return redirect("checkout_done", order_id=order.order_id)

def checkout_done(request, order_id: int):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "checkout_done.html", {"order": order})