from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    menu, view_cart,
    customize_pizza,
    add_to_cart, add_drink_to_cart, add_dessert_to_cart,
    remove_cart_item, clear_cart, checkout, checkout_done,
    signup, my_orders, cancel_order,
    report_undelivered, report_top3_month, report_earnings,
)

urlpatterns = [
    path("", menu, name="menu"),

    path("customize/<int:pizza_id>/", customize_pizza, name="customize_pizza"),

    path("cart/", view_cart, name="view_cart"),
    path("cart/add/<int:pizza_id>/", add_to_cart, name="add_to_cart"),
    path("cart/add/drink/<int:drink_id>/", add_drink_to_cart, name="add_drink_to_cart"),
    path("cart/add/dessert/<int:dessert_id>/", add_dessert_to_cart, name="add_dessert_to_cart"),
    path("cart/remove/<str:kind>/<int:item_id>/", remove_cart_item, name="remove_cart_item"),
    path("cart/clear/", clear_cart, name="clear_cart"),
    path("checkout/", checkout, name="checkout"),
    path("checkout/done/<int:order_id>/", checkout_done, name="checkout_done"),

    # Accounts
    path("accounts/signup/", signup, name="signup"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="menu"), name="logout"),

    path("orders/my/", my_orders, name="my_orders"),
    path("orders/cancel/<int:order_id>/", cancel_order, name="cancel_order"),

    path("reports/undelivered/", report_undelivered, name="report_undelivered"),
    path("reports/top3-month/", report_top3_month, name="report_top3_month"),
    path("reports/earnings/", report_earnings, name="report_earnings"),
]
