# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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
    availability = models.IntegerField(blank=True, null=True)
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
    sugar_free = models.IntegerField(blank=True, null=True)
    gluten_free = models.IntegerField(blank=True, null=True)
    milk_free = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    availability = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dessert'


class Discountcode(models.Model):
    discount_id = models.AutoField(primary_key=True)
    discount_code = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=255, blank=True, null=True)
    discount_value = models.IntegerField()
    discount_type = models.CharField(max_length=7)
    valid_from = models.DateField(blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DiscountCode'


class Discountredemption(models.Model):
    redemption_id = models.AutoField(primary_key=True)
    discount = models.ForeignKey(Discountcode, models.DO_NOTHING)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    order = models.ForeignKey('Order', models.DO_NOTHING)
    redeemed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DiscountRedemption'
        unique_together = (('discount', 'order'),)


class Drink(models.Model):
    drink_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    milk_free = models.IntegerField(blank=True, null=True)
    sugar_free = models.IntegerField(blank=True, null=True)
    volume_ml = models.IntegerField(blank=True, null=True)
    is_alcoholic = models.IntegerField(blank=True, null=True)
    availability = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Drink'


class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    vegan = models.IntegerField(blank=True, null=True)
    vegetarian = models.IntegerField(blank=True, null=True)
    allergen = models.IntegerField(blank=True, null=True)
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
    is_active = models.IntegerField(blank=True, null=True)
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
    product_type = models.CharField(max_length=7)
    display_order = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MenuItems'
        unique_together = (('menu', 'product_id', 'product_type'),)


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
    pizza = models.ForeignKey('Pizza', models.DO_NOTHING, blank=True, null=True)
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


class Pizza(models.Model):
    pizza_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=3)
    availability = models.IntegerField(blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_vegetarian = models.IntegerField(blank=True, null=True)
    is_vegan = models.IntegerField(blank=True, null=True)
    is_gluten_free = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Pizza'
        unique_together = (('name', 'size'),)


class PizzaIngredients(models.Model):
    pk = models.CompositePrimaryKey('pizza_id', 'ingredient_id')
    pizza = models.ForeignKey(Pizza, models.DO_NOTHING)
    ingredient = models.ForeignKey(Ingredient, models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Pizza_Ingredients'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class Pizzapriceview(models.Model):
    pizza_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=3)
    ingredients_cost = models.DecimalField(max_digits=10, decimal_places=2)
    price_no_vat = models.DecimalField(max_digits=10, decimal_places=2)
    price_with_vat = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "PizzaPriceView"
