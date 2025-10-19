from django.contrib import admin
from . import models

def _register_all():
    for name in dir(models):
        obj = getattr(models, name)
        try:
            if issubclass(obj, models.models.Model) and obj is not models.models.Model:
                if getattr(obj._meta, "db_table", "").lower() == "pizzapriceview":
                    continue
                admin.site.register(obj)
        except Exception:
            pass

_register_all()
