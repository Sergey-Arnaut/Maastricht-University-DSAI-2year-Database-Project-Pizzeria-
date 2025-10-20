from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Let the core app own the root ("/") so the menu at "" works
    path("", include("core.urls")),
]
