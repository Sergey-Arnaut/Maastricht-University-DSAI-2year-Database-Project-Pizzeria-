from django.shortcuts import render
from .models import Pizzapriceview, Pizza

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
