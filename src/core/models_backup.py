from django.db import models

class Pizzapriceview(models.Model):
    pizza_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=3)
    ingredients_cost = models.DecimalField(max_digits=10, decimal_places=2)
    price_no_vat = models.DecimalField(max_digits=10, decimal_places=2)
    price_with_vat = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False          # это VIEW
        db_table = "PizzaPriceView"
