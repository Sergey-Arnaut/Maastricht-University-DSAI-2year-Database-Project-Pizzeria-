from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    # Menu & cart / checkout
    menu, view_cart, add_to_cart, remove_from_cart, clear_cart,
    checkout, checkout_done,

    # Accounts
    signup,

    # My orders
    my_orders, cancel_order,

    # Staff reports
    report_undelivered, report_top3_month, report_earnings,
)

urlpatterns = [
    # Menu
    path("", menu, name="menu"),

    # Cart / checkout
    path("cart/", view_cart, name="view_cart"),
    path("cart/add/<int:pizza_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:pizza_id>/", remove_from_cart, name="remove_from_cart"),
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
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="start"),  # back to "/" then to login/menu via start view
        name="logout",
    ),

    # My orders
    path("orders/my/", my_orders, name="my_orders"),
    path("orders/cancel/<int:order_id>/", cancel_order, name="cancel_order"),

    # Staff reports
    path("reports/undelivered/", report_undelivered, name="report_undelivered"),
    path("reports/top3-month/", report_top3_month, name="report_top3_month"),
    path("reports/earnings/", report_earnings, name="report_earnings"),
]
