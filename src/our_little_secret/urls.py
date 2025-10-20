# src/our_little_secret/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def start_view(request):
    """
    Root (/) behavior:
      - if authenticated -> go to menu
      - else -> go to login
    """
    if request.user.is_authenticated:
        return redirect("menu")
    return redirect("login")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", start_view, name="start"),   # << smart start page
    path("", include("core.urls")),       # app routes
]
