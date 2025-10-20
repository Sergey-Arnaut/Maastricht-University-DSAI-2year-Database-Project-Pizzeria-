from django.contrib import admin
from django.db import models as dj_models
from . import models
from .models_view import Pizzapriceview

@admin.register(Pizzapriceview)
class PizzaPriceViewAdmin(admin.ModelAdmin):
    list_display = ("pizza_id", "name", "size", "ingredients_cost", "price_no_vat", "price_with_vat")
    readonly_fields = list_display
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False

def _register_all_models():
    for name in dir(models):
        obj = getattr(models, name)
        if isinstance(obj, type) and issubclass(obj, dj_models.Model) and obj is not dj_models.Model:
            if getattr(getattr(obj, "_meta", None), "app_label", "") != "core":
                continue
            if getattr(obj._meta, "db_table", "").lower() == "pizzapriceview":
                continue
            try:
                admin.site.register(obj)
            except admin.sites.AlreadyRegistered:
                pass

_register_all_models()
