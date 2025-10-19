from django.urls import path
from .views import (
    menu, view_cart, add_to_cart, remove_from_cart, clear_cart, checkout, checkout_done
)

urlpatterns = [
    path("", menu, name="menu"),
    path("cart/", view_cart, name="view_cart"),
    path("cart/add/<int:pizza_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:pizza_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/clear/", clear_cart, name="clear_cart"),
    path("checkout/", checkout, name="checkout"),
    path("checkout/done/<int:order_id>/", checkout_done, name="checkout_done"),
]
