
from django.db import models


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    postal_code = models.CharField(max_length=12, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Customer'


class Deliveryperson(models.Model):
    delivery_person_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    number_of_orders = models.IntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    availability = models.BooleanField(blank=True, null=True)
    current_position = models.CharField(max_length=255, blank=True, null=True)
    delivery_postal_code = models.CharField(max_length=12, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DeliveryPerson'


class Dessert(models.Model):
    dessert_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sugar_free = models.BooleanField(blank=True, null=True)
    gluten_free = models.BooleanField(blank=True, null=True)
    milk_free = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    availability = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dessert'


class Discountcode(models.Model):
    discount_id = models.AutoField(primary_key=True)
    discount_code = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=255, blank=True, null=True)
    discount_value = models.IntegerField()
    discount_type = models.CharField(max_length=7)  # 'percent' or 'value'
    valid_from = models.DateField(blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DiscountCode'


class Drink(models.Model):
    drink_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    milk_free = models.BooleanField(blank=True, null=True)
    sugar_free = models.BooleanField(blank=True, null=True)
    volume_ml = models.IntegerField(blank=True, null=True)
    is_alcoholic = models.BooleanField(blank=True, null=True)
    availability = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Drink'


class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    vegan = models.BooleanField(blank=True, null=True)
    vegetarian = models.BooleanField(blank=True, null=True)
    allergen = models.BooleanField(blank=True, null=True)
    allergen_type = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=20, blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Ingredient'


class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    menu_name = models.CharField(max_length=100)
    is_active = models.BooleanField(blank=True, null=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Menu'


class Menuitems(models.Model):
    menu_item_id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(Menu, models.DO_NOTHING)
    product_id = models.IntegerField()
    product_type = models.CharField(max_length=7)  # 'pizza' | 'drink' | 'dessert'
    display_order = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MenuItems'
        unique_together = (('menu', 'product_id', 'product_type'),)


class Pizza(models.Model):
    pizza_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=3)  # 'S','M','L','XL','XXL'
    availability = models.BooleanField(blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_vegetarian = models.BooleanField(blank=True, null=True)
    is_vegan = models.BooleanField(blank=True, null=True)
    is_gluten_free = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Pizza'
        unique_together = (('name', 'size'),)


class PizzaIngredients(models.Model):
    # Surrogate PK instead of CompositePrimaryKey
    id = models.AutoField(primary_key=True)
    pizza = models.ForeignKey(Pizza, models.DO_NOTHING)
    ingredient = models.ForeignKey(Ingredient, models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Pizza_Ingredients'
        unique_together = (('pizza', 'ingredient'),)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    order_timestamp = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_postal_code = models.CharField(max_length=12)
    delivery_person = models.ForeignKey(Deliveryperson, models.DO_NOTHING, blank=True, null=True)
    estimated_delivery_time = models.DateTimeField(blank=True, null=True)
    actual_delivery_time = models.DateTimeField(blank=True, null=True)
    discount = models.ForeignKey(Discountcode, models.DO_NOTHING, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_id = models.IntegerField(blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Order'


class Orderitem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, models.DO_NOTHING)
    pizza = models.ForeignKey(Pizza, models.DO_NOTHING, blank=True, null=True)
    ingredient = models.ForeignKey(Ingredient, models.DO_NOTHING, blank=True, null=True)
    pizza_quantity = models.IntegerField(blank=True, null=True)
    drink = models.ForeignKey(Drink, models.DO_NOTHING, blank=True, null=True)
    drink_quantity = models.IntegerField(blank=True, null=True)
    dessert = models.ForeignKey(Dessert, models.DO_NOTHING, blank=True, null=True)
    dessert_quantity = models.IntegerField(blank=True, null=True)
    item_current_price = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'OrderItem'


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, models.DO_NOTHING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=6)
    status = models.CharField(max_length=9, blank=True, null=True)
    payment_timestamp = models.DateTimeField(blank=True, null=True)
    refund_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Payment'


class Discountredemption(models.Model):
    redemption_id = models.AutoField(primary_key=True)
    discount = models.ForeignKey(Discountcode, models.DO_NOTHING)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    order = models.ForeignKey(Order, models.DO_NOTHING)
    redeemed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DiscountRedemption'
        unique_together = (('discount', 'order'),)
