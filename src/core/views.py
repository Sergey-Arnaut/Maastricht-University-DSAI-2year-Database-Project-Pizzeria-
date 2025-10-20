# src/core/views.py
from datetime import datetime, date, timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction, connection
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import (
    Customer, Pizza, Order, Orderitem,
    Discountcode, Discountredemption, Deliveryperson, Drink
)
from .models_view import Pizzapriceview
from .forms import SignUpForm

CANCELLATION_MINUTES = 5

# 👉 Hard-coded vouchers (case-insensitive)
VOUCHER_MAP = {
    "PEPPELS": 15,   # 15% off
    "LENA": 20,      # 20% off
    "SEREJA": 25,    # 25% off
}

def _get_cart(request):
    return request.session.get("cart", {})

def _save_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True

def _current_customer(request) -> Customer:
    if not request.user.is_authenticated:
        cust, _ = Customer.objects.get_or_create(
            email="demo@example.com",
            defaults=dict(first_name="Demo", last_name="User", postal_code="62150", date_of_birth=date(2000, 10, 1)),
        )
        return cust

    email = request.user.email or f"{request.user.username}@example.local"
    defaults = dict(first_name=request.user.first_name or "", last_name=request.user.last_name or "")
    cust, _ = Customer.objects.get_or_create(email=email, defaults=defaults)
    changed = False
    if request.user.first_name and cust.first_name != request.user.first_name:
        cust.first_name = request.user.first_name; changed = True
    if request.user.last_name and cust.last_name != request.user.last_name:
        cust.last_name = request.user.last_name; changed = True
    if changed:
        cust.save(update_fields=["first_name", "last_name"])
    return cust

def _fetch_cart_rows(cart: dict):
    if not cart:
        return [], Decimal("0.00")
    ids = [int(k) for k in cart.keys()]
    pizzas = {p.pizza_id: p for p in Pizza.objects.filter(pizza_id__in=ids)}
    pv_map = {v.pizza_id: v for v in Pizzapriceview.objects.filter(pizza_id__in=ids)}
    rows, subtotal = [], Decimal("0.00")
    for pid, qty in cart.items():
        p = pizzas.get(int(pid))
        if not p:
            continue
        v = pv_map.get(int(pid))
        unit = (v.price_with_vat if v else Decimal(p.base_price or 0))
        line = unit * Decimal(int(qty))
        rows.append({"pizza": p, "qty": int(qty), "unit": unit, "sum": line})
        subtotal += line
    return rows, subtotal.quantize(Decimal("0.01"))

def _customer_total_pizzas(customer_id: int) -> int:
    with connection.cursor() as cur:
        cur.execute("""
            SELECT COALESCE(SUM(oi.pizza_quantity), 0)
            FROM OrderItem oi
            JOIN `Order` o ON o.order_id = oi.order_id
            WHERE o.customer_id = %s
              AND o.status IN ('delivered','ready','out_for_delivery','baking','preparing','pending')
        """, [customer_id])
        row = cur.fetchone()
    return int(row[0] or 0)

def _birthday_freebies_discount(order_rows, drinks_qs):
    discount = Decimal("0.00")
    if order_rows:
        cheapest_pizza = min((r["unit"] for r in order_rows), default=Decimal("0.00"))
        discount += cheapest_pizza
    d = drinks_qs.filter(availability=True).order_by("price").first()
    if d:
        discount += Decimal(d.price or 0)
    return discount.quantize(Decimal("0.01"))

def _ensure_voucher_code_object(code_text: str) -> Discountcode | None:
    """
    If code_text is one of our hard-coded vouchers, ensure there's a DiscountCode row.
    Returns the DiscountCode if applicable, else None.
    """
    pct = VOUCHER_MAP.get(code_text.upper())
    if not pct:
        return None
    today = date.today()
    obj, _ = Discountcode.objects.get_or_create(
        discount_code=code_text.upper(),
        defaults=dict(
            password=None,
            discount_value=pct,
            discount_type="percent",
            valid_from=today - timedelta(days=1),
            valid_until=today + timedelta(days=365),
            is_active=True,
        ),
    )
    # If existing but inactive/expired, make it usable (dev convenience)
    changed = False
    if not obj.is_active:
        obj.is_active = True; changed = True
    if obj.valid_until and obj.valid_until < today:
        obj.valid_until = today + timedelta(days=365); changed = True
    if changed:
        obj.save(update_fields=["is_active", "valid_until"])
    return obj

def _apply_discounts_spec(customer: Customer, rows, subtotal: Decimal, discount_code_input: str):
    applied = {}
    discount_total = Decimal("0.00")
    code_obj = None

    if _customer_total_pizzas(customer.customer_id) >= 10:
        loyalty_disc = (subtotal * Decimal("0.10")).quantize(Decimal("0.01"))
        if loyalty_disc > 0:
            applied["loyalty_10pct"] = str(loyalty_disc)
            discount_total += loyalty_disc

    if customer.date_of_birth and customer.date_of_birth.month == date.today().month and customer.date_of_birth.day == date.today().day:
        bday_disc = _birthday_freebies_discount(rows, Drink.objects)
        if bday_disc > 0:
            applied["birthday_freebies"] = str(bday_disc)
            discount_total += bday_disc

    code_text = (discount_code_input or "").strip()
    if code_text:
        # 👉 allow our hard-coded vouchers
        maybe_voucher = _ensure_voucher_code_object(code_text)
        try:
            code = Discountcode.objects.get(discount_code=code_text.upper() if maybe_voucher else code_text, is_active=True)
            today = date.today()
            if (code.valid_from and today < code.valid_from) or (code.valid_until and today > code.valid_until):
                code = None
        except Discountcode.DoesNotExist:
            code = None

        if code and not Discountredemption.objects.filter(discount_id=code.discount_id).exists():
            if code.discount_type == "percent":
                val = (subtotal * Decimal(code.discount_value) / Decimal("100")).quantize(Decimal("0.01"))
            else:
                val = Decimal(code.discount_value).quantize(Decimal("0.01"))
            if val > 0:
                applied[f"code_{code.discount_code}"] = str(val)
                discount_total += val
                code_obj = code

    total = (subtotal - discount_total)
    if total < 0:
        total = Decimal("0.00")
    return total.quantize(Decimal("0.01")), discount_total.quantize(Decimal("0.01")), applied, code_obj

def _assign_delivery(order_id: int, delivery_postal_code: str):
    with connection.cursor() as cur:
        cur.execute("""
            SELECT dp.delivery_person_id
            FROM DeliveryPerson dp
            WHERE dp.availability = TRUE
              AND dp.delivery_postal_code = %s
              AND NOT EXISTS (
                    SELECT 1
                    FROM `Order` o2
                    WHERE o2.delivery_person_id = dp.delivery_person_id
                      AND o2.status = 'delivered'
                      AND o2.actual_delivery_time >= (NOW() - INTERVAL 30 MINUTE)
              )
            ORDER BY dp.number_of_orders ASC, dp.rating DESC
            LIMIT 1
        """, [delivery_postal_code])
        row = cur.fetchone()

    if not row:
        return None

    dp_id = int(row[0])
    with transaction.atomic():
        with connection.cursor() as cur:
            cur.execute("UPDATE `Order` SET delivery_person_id=%s WHERE order_id=%s", [dp_id, order_id])
            cur.execute("UPDATE DeliveryPerson SET number_of_orders = number_of_orders + 1 WHERE delivery_person_id=%s",
                        [dp_id])
    return dp_id

def menu(request):
    cart = _get_cart(request)
    pizzas = list(Pizza.objects.filter(availability=True)[:100])
    price_map = {v.pizza_id: v for v in Pizzapriceview.objects.filter(pizza_id__in=[p.pizza_id for p in pizzas])}
    items = []
    for p in pizzas:
        v = price_map.get(p.pizza_id)
        items.append({
            "id": p.pizza_id,
            "name": (v.name if v else p.name),
            "size": p.size,
            "is_vegan": bool(getattr(p, "is_vegan", False)),
            "is_vegetarian": bool(getattr(p, "is_vegetarian", False)),
            "price": (v.price_with_vat if v else p.base_price),
        })
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
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, "Корзина пуста.")
        return redirect("menu")

    customer = _current_customer(request)
    rows, subtotal = _fetch_cart_rows(cart)
    total, discount_amount, applied, code_obj = _apply_discounts_spec(
        customer, rows, subtotal, request.POST.get("discount_code", "")
    )

    with transaction.atomic():
        order = Order.objects.create(
            customer_id=customer.customer_id,
            order_timestamp=datetime.now(),
            status="pending",
            total_price=total,
            delivery_postal_code=(customer.postal_code or "00000"),
            discount_id=(code_obj.discount_id if code_obj else None),
            discount_amount=discount_amount,
        )
        for r in rows:
            Orderitem.objects.create(
                order_id=order.order_id,
                pizza_id=r["pizza"].pizza_id,
                pizza_quantity=r["qty"],
                item_current_price=r["unit"],
            )
        if code_obj:
            Discountredemption.objects.create(
                discount_id=code_obj.discount_id,
                customer_id=customer.customer_id,
                order_id=order.order_id,
            )
            Discountcode.objects.filter(discount_id=code_obj.discount_id).update(is_active=False)

        dp_id = _assign_delivery(order.order_id, order.delivery_postal_code)
        if dp_id:
            Order.objects.filter(order_id=order.order_id).update(status="preparing")

    _save_cart(request, {})
    if dp_id:
        messages.success(request, f"Заказ №{order.order_id} создан. Скидки: {discount_amount}€")
    else:
        messages.warning(request, f"Заказ №{order.order_id} создан, но курьер не найден на ближайшие 30 минут.")
    return redirect("checkout_done", order_id=order.order_id)

def checkout_done(request, order_id: int):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "checkout_done.html", {"order": order})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            from django.contrib.auth.models import User
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
                first_name=form.cleaned_data.get("first_name", ""),
                last_name=form.cleaned_data.get("last_name", ""),
            )
            cust, _ = Customer.objects.get_or_create(
                email=user.email,
                defaults=dict(
                    first_name=user.first_name,
                    last_name=user.last_name,
                    postal_code=form.cleaned_data.get("postal_code") or "",
                    date_of_birth=form.cleaned_data.get("date_of_birth"),
                ),
            )
            to_update = []
            if form.cleaned_data.get("postal_code") and cust.postal_code != form.cleaned_data["postal_code"]:
                cust.postal_code = form.cleaned_data["postal_code"]; to_update.append("postal_code")
            if form.cleaned_data.get("date_of_birth") and cust.date_of_birth != form.cleaned_data["date_of_birth"]:
                cust.date_of_birth = form.cleaned_data["date_of_birth"]; to_update.append("date_of_birth")
            if to_update:
                cust.save(update_fields=to_update)

            login(request, user)
            messages.success(request, "Welcome! Account created.")
            return redirect("menu")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def my_orders(request):
    cust = _current_customer(request)
    orders = Order.objects.filter(customer_id=cust.customer_id).order_by("-order_timestamp")[:200]
    now = timezone.now()
    annotated = []
    for o in orders:
        placed = o.order_timestamp
        if placed and not timezone.is_aware(placed):
            placed = timezone.make_aware(placed, timezone.utc)
        minutes_since = (now - placed).total_seconds() / 60 if placed else 9999
        cancellable = (o.status in ("pending", "preparing")) and (minutes_since <= CANCELLATION_MINUTES)
        annotated.append((o, cancellable, max(0, int(CANCELLATION_MINUTES - minutes_since))))
    return render(request, "orders/my_orders.html", {"orders": annotated, "cancel_window": CANCELLATION_MINUTES})

@login_required
@require_POST
def cancel_order(request, order_id: int):
    cust = _current_customer(request)
    order = get_object_or_404(Order, pk=order_id, customer_id=cust.customer_id)
    if order.status not in ("pending", "preparing"):
        messages.warning(request, "Order can no longer be cancelled.")
        return redirect("my_orders")

    now = timezone.now()
    placed = order.order_timestamp
    if placed and not timezone.is_aware(placed):
        placed = timezone.make_aware(placed, timezone.utc)
    minutes_since = (now - placed).total_seconds() / 60 if placed else 9999
    if minutes_since > CANCELLATION_MINUTES:
        messages.warning(request, f"Cancellation window ({CANCELLATION_MINUTES} min) has passed.")
        return redirect("my_orders")

    with transaction.atomic():
        Order.objects.filter(order_id=order.order_id).update(status="cancelled")
    messages.success(request, f"Order #{order.order_id} cancelled.")
    return redirect("my_orders")

# ---------- Staff reports (unchanged from previous message) ----------
def _staff_required(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@user_passes_test(_staff_required)
def report_undelivered(request):
    orders = Order.objects.exclude(status__in=["delivered", "cancelled"]).order_by("-order_timestamp")[:300]
    return render(request, "reports/undelivered.html", {"orders": orders})

@user_passes_test(_staff_required)
def report_top3_month(request):
    cutoff = timezone.now() - timedelta(days=30)
    qs = (
        Orderitem.objects
        .filter(
            pizza__isnull=False,
            order__order_timestamp__gte=cutoff,
            order__status__in=["delivered", "out_for_delivery", "ready", "baking", "preparing"],
        )
        .values("pizza__name", "pizza__size")
        .annotate(total=Sum("pizza_quantity"))
        .order_by("-total")[:3]
    )
    return render(request, "reports/top3_month.html", {"rows": qs, "since": cutoff})

@user_passes_test(_staff_required)
def report_earnings(request):
    by = request.GET.get("by", "gender")
    delivered = Order.objects.filter(status="delivered")
    rows = []
    if by == "postal":
        data = delivered.values("customer__postal_code").annotate(sum_total=Sum("total_price")).order_by("-sum_total")
        rows = [{"label": r["customer__postal_code"] or "—", "sum": r["sum_total"] or 0} for r in data]
    elif by == "age":
        buckets = {"<25": Decimal("0.00"), "25-34": Decimal("0.00"), "35-49": Decimal("0.00"), "50+": Decimal("0.00")}
        today = date.today()
        data = delivered.select_related("customer").values("total_price", "customer__date_of_birth")
        for r in data:
            dob = r["customer__date_of_birth"]; amount = Decimal(r["total_price"] or 0)
            if not dob: continue
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 25: buckets["<25"] += amount
            elif age < 35: buckets["25-34"] += amount
            elif age < 50: buckets["35-49"] += amount
            else: buckets["50+"] += amount
        rows = [{"label": k, "sum": v} for k, v in buckets.items()]
    else:
        data = delivered.values("customer__gender").annotate(sum_total=Sum("total_price")).order_by("-sum_total")
        rows = [{"label": (r["customer__gender"] or "—"), "sum": r["sum_total"] or 0} for r in data]
    total = sum(Decimal(r["sum"]) for r in rows) if rows else Decimal("0.00")
    return render(request, "reports/earnings.html", {"rows": rows, "group_by": by, "total": total})
