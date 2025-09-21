from django.urls import path
from .views import menu

urlpatterns = [
    path("", menu, name="menu"),
]
