# src/core/models_view.py
from django.db import models

class Pizzapriceview(models.Model):
    pizza_id = models.IntegerField(primary_key=True)
    # map to DB columns in your current MySQL VIEW
    name = models.CharField(max_length=100, db_column="pizza_name")
    size = models.CharField(max_length=3)
    ingredients_cost = models.DecimalField(max_digits=10, decimal_places=2, db_column="ingredients_cost")
    price_no_vat = models.DecimalField(max_digits=10, decimal_places=2, db_column="price_before_vat")
    price_with_vat = models.DecimalField(max_digits=10, decimal_places=2, db_column="final_price")

    class Meta:
        managed = False
        db_table = "PizzaPriceView"
