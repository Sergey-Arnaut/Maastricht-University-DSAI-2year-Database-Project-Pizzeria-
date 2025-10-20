import mysql.connector
import os

db_config = {
    'host': 'mysql-bccc7a6-sergey-1c63.h.aivencloud.com',
    'user': 'lena',
    'password': 'Ols1-2025',
    'database': 'our_little_secret',
    'port': 28373,
    'ssl_ca': 'ca.pem',
    'ssl_verify_cert': True
}


def create_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        print("Successful connection to db:))")
        return conn
    except mysql.connector.Error as e:
        print(f"Mistake with connection to db: {e}")
        return None


def run_sql_file(conn, filename):
    try:
        cursor = conn.cursor()
        with open(filename, "r", encoding="utf-8") as f:
            sql_script = f.read()

        for statement in sql_script.split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)

        conn.commit()
        print(f"file '{filename}' is executed successfully")

    except Exception as e:
        print(f"Error with '{filename}': {e}")


def create_pizza_price_view(conn):
    try:
        cursor = conn.cursor()

        view_sql = """
        CREATE OR REPLACE VIEW PizzaPriceView AS
        SELECT 
            p.pizza_id,
            p.name AS pizza_name,
            p.size,
            p.base_price,
            SUM(pi.quantity * i.price_per_unit) AS ingredients_cost,
            ROUND(SUM(pi.quantity * i.price_per_unit) * 1.5, 2) AS price_before_vat,
            ROUND(SUM(pi.quantity * i.price_per_unit) * 1.5 * 1.2, 2) AS final_price
        FROM Pizza p
        JOIN Pizza_Ingredients pi ON p.pizza_id = pi.pizza_id
        JOIN Ingredient i ON pi.ingredient_id = i.ingredient_id
        GROUP BY p.pizza_id, p.name, p.size, p.base_price;
        """

        cursor.execute(view_sql)
        conn.commit()
        print("Success")
        return True

    except mysql.connector.Error as e:
        print(f"Error with: {e}")
        return False


def retrieve_menu_data(conn):
    try:
        cursor = conn.cursor(dictionary=True)

        print("\nMenu")
        print("=" * 50)

        cursor.execute("SELECT * FROM PizzaPriceView;")
        rows = cursor.fetchall()

        for row in rows:
            print(f"{row['pizza_name']} ({row['size']}): {row['final_price']} EUR")

        return rows

    except mysql.connector.Error as e:
        print(f"Error with: {e}")
        return []


def get_undelivered_orders(conn):
    try:
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            o.order_id,
            o.customer_id,
            c.first_name,
            c.last_name,
            o.status,
            o.order_timestamp,
            o.total_price,
            o.delivery_postal_code,
            o.estimated_delivery_time,
            TIMESTAMPDIFF(MINUTE, o.order_timestamp, NOW()) AS minutes_pending
        FROM `Order` o
        JOIN Customer c ON o.customer_id = c.customer_id
        WHERE o.status NOT IN ('delivered', 'cancelled')
        ORDER BY o.order_timestamp ASC;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        print("\nUndelivered orders")
        print("=" * 60)

        if not results:
            print("All orders have been delivered/cancelled")
            return []

        for row in results:
            print(f"Order #{row['order_id']} - Status: {row['status']}")
            print(f"   Customer: {row['first_name']} {row['last_name']}")
            print(f"   Ordered: {row['order_timestamp']}")
            print(f"   Total: {row['total_price']} EUR")
            print(f"   Delivery to: {row['delivery_postal_code']}")
            print(f"   Pending for: {row['minutes_pending']} minutes")
            print("-" * 40)

        return results

    except mysql.connector.Error as e:
        print(f"Error retrieving undelivered orders: {e}")
        return []

def get_delivery_earnings_by_gender(conn):
    try:
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            dp.gender,
            COUNT(DISTINCT dp.delivery_person_id) AS delivery_persons_count,
            SUM(der.completed_deliveries) AS total_deliveries,
            SUM(der.restaurant_revenue) AS total_revenue,
            AVG(der.total_earnings) AS avg_earnings,
            SUM(der.total_earnings) AS total_earnings
        FROM DeliveryPerson dp
        JOIN DeliveryEarningsReport der ON dp.delivery_person_id = der.delivery_person_id
        GROUP BY dp.gender
        ORDER BY total_earnings DESC;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        print("\nDELIVERY EARNINGS BY GENDER")
        print("=" * 60)

        if not results:
            print("No data found")
            return []

        for row in results:
            gender_display = row['gender'] if row['gender'] else 'Not specified'
            print(f"  {gender_display}:")
            print(f"    Delivery Persons: {row['delivery_persons_count']}")
            print(f"    Total Deliveries: {row['total_deliveries']}")
            print(f"    Restaurant Revenue: {row['total_revenue']:.2f} EUR")
            print(f"    Average Earnings: {row['avg_earnings']:.2f} EUR")
            print(f"    Total Earnings: {row['total_earnings']:.2f} EUR")
            print("-" * 40)

        return results

    except mysql.connector.Error as e:
        print(f"Error retrieving delivery earnings by gender: {e}")
        return []

    except mysql.connector.Error as e:
        print(f"Error retrieving earnings by gender: {e}")
        return []

def get_delivery_earnings_by_age(conn):
    try:
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            der.age_group,
            COUNT(DISTINCT der.delivery_person_id) AS delivery_persons_count,
            SUM(der.completed_deliveries) AS total_deliveries,
            SUM(der.restaurant_revenue) AS total_revenue,
            AVG(der.total_earnings) AS avg_earnings,
            SUM(der.total_earnings) AS total_earnings
        FROM DeliveryEarningsReport der
        GROUP BY der.age_group
        ORDER BY total_earnings DESC;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        print("\nDELIVERY EARNINGS BY AGE GROUP")
        print("=" * 60)

        if not results:
            print("No data found")
            return []

        for row in results:
            print(f"  Age {row['age_group']}:")
            print(f"    Delivery Persons: {row['delivery_persons_count']}")
            print(f"    Total Deliveries: {row['total_deliveries']}")
            print(f"    Restaurant Revenue: {row['total_revenue']:.2f} EUR")
            print(f"    Average Earnings: {row['avg_earnings']:.2f} EUR")
            print(f"    Total Earnings: {row['total_earnings']:.2f} EUR")
            print("-" * 40)

        return results

    except mysql.connector.Error as e:
        print(f"Error retrieving delivery earnings by age: {e}")
        return []

def get_delivery_earnings_by_postal_code(conn):
    try:
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            der.delivery_postal_code,
            COUNT(DISTINCT der.delivery_person_id) AS delivery_persons_count,
            SUM(der.completed_deliveries) AS total_deliveries,
            SUM(der.restaurant_revenue) AS total_revenue,
            AVG(der.total_earnings) AS avg_earnings,
            SUM(der.total_earnings) AS total_earnings
        FROM DeliveryEarningsReport der
        GROUP BY der.delivery_postal_code
        ORDER BY total_earnings DESC;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        print("\nDELIVERY EARNINGS BY POSTAL CODE")
        print("=" * 60)

        if not results:
            print("No data found")
            return []

        for row in results:
            print(f"  Postal Code: {row['delivery_postal_code']}")
            print(f"    Delivery Persons: {row['delivery_persons_count']}")
            print(f"    Total Deliveries: {row['total_deliveries']}")
            print(f"    Restaurant Revenue: {row['total_revenue']:.2f} EUR")
            print(f"    Average Earnings: {row['avg_earnings']:.2f} EUR")
            print(f"    Total Earnings: {row['total_earnings']:.2f} EUR")
            print("-" * 40)

        return results

    except mysql.connector.Error as e:
        print(f"Error retrieving delivery earnings by postal code: {e}")
        return []

def place_order_transaction(conn, customer_id, order_items, delivery_postal_code, discount_id=None):
    cursor = None
    try:
        conn.start_transaction()
        cursor = conn.cursor(dictionary=True)

        print("Start of the order transaction")

        cursor.execute("SELECT customer_id FROM Customer WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        if not customer:
            raise Exception(f"Customer with ID {customer_id} not found")

        total_price = 0
        discount_amount = 0

        for item in order_items:
            if 'pizza_id' in item and item['pizza_id']:
                cursor.execute("SELECT base_price FROM Pizza WHERE pizza_id = %s AND availability = TRUE",
                               (item['pizza_id'],))
                pizza = cursor.fetchone()
                if not pizza:
                    raise Exception(f"Pizza with ID {item['pizza_id']} not available")
                total_price += pizza['base_price'] * item.get('quantity', 1)

            elif 'drink_id' in item and item['drink_id']:
                cursor.execute("SELECT price FROM Drink WHERE drink_id = %s AND availability = TRUE",
                               (item['drink_id'],))
                drink = cursor.fetchone()
                if not drink:
                    raise Exception(f"Drink with ID {item['drink_id']} not available")
                total_price += drink['price'] * item.get('quantity', 1)

            elif 'dessert_id' in item and item['dessert_id']:
                cursor.execute("SELECT price FROM Dessert WHERE dessert_id = %s AND availability = TRUE",
                               (item['dessert_id'],))
                dessert = cursor.fetchone()
                if not dessert:
                    raise Exception(f"Dessert with ID {item['dessert_id']} not available")
                total_price += dessert['price'] * item.get('quantity', 1)

        if discount_id:
            cursor.execute("""
                SELECT discount_value, discount_type 
                FROM DiscountCode 
                WHERE discount_id = %s AND is_active = TRUE 
                AND (valid_until IS NULL OR valid_until >= CURDATE())
            """, (discount_id,))
            discount = cursor.fetchone()
            if discount:
                if discount['discount_type'] == 'percent':
                    discount_amount = total_price * discount['discount_value'] / 100
                else:
                    discount_amount = min(discount['discount_value'], total_price)
                total_price = max(0, total_price - discount_amount)
            else:
                discount_id = None

        insert_order_sql = """
        INSERT INTO `Order` (customer_id, total_price, delivery_postal_code, discount_id, discount_amount, status)
        VALUES (%s, %s, %s, %s, %s, 'pending')
        """
        cursor.execute(insert_order_sql, (customer_id, total_price, delivery_postal_code, discount_id, discount_amount))
        order_id = cursor.lastrowid

        print(f"Order #{order_id} created")

        for item in order_items:
            if 'pizza_id' in item and item['pizza_id']:
                cursor.execute("SELECT base_price FROM Pizza WHERE pizza_id = %s", (item['pizza_id'],))
                pizza = cursor.fetchone()
                insert_item_sql = """
                INSERT INTO OrderItem (order_id, pizza_id, pizza_quantity, item_current_price)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_item_sql,
                               (order_id, item['pizza_id'], item.get('quantity', 1), pizza['base_price']))

            elif 'drink_id' in item and item['drink_id']:
                cursor.execute("SELECT price FROM Drink WHERE drink_id = %s", (item['drink_id'],))
                drink = cursor.fetchone()
                insert_item_sql = """
                INSERT INTO OrderItem (order_id, drink_id, drink_quantity, item_current_price)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_item_sql, (order_id, item['drink_id'], item.get('quantity', 1), drink['price']))

            elif 'dessert_id' in item and item['dessert_id']:
                cursor.execute("SELECT price FROM Dessert WHERE dessert_id = %s", (item['dessert_id'],))
                dessert = cursor.fetchone()
                insert_item_sql = """
                INSERT INTO OrderItem (order_id, dessert_id, dessert_quantity, item_current_price)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_item_sql,
                               (order_id, item['dessert_id'], item.get('quantity', 1), dessert['price']))

        print(f"Added {len(order_items)} items to order")

        #Creating the payment
        insert_payment_sql = """
        INSERT INTO Payment (order_id, amount, payment_method, status)
        VALUES (%s, %s, 'card', 'pending')
        """
        cursor.execute(insert_payment_sql, (order_id, total_price))
        payment_id = cursor.lastrowid

        cursor.execute("UPDATE `Order` SET payment_id = %s WHERE order_id = %s", (payment_id, order_id))

        print(f"Payment #{payment_id} created")

        if discount_id:
            insert_redemption_sql = """
            INSERT INTO DiscountRedemption (discount_id, customer_id, order_id)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_redemption_sql, (discount_id, customer_id, order_id))
            print("Discount applied and marked")

        conn.commit()
        print(f"ORDER #{order_id} SUCCESSFULLY PLACED")
        print(f"   Total: {total_price:.2f} euro")
        print(f"   Discount: {discount_amount:.2f} euro")
        print(f"   Delivery to: {delivery_postal_code}")

        return order_id

    except Exception as e:
        print(f"Error: {e}")
        print("Rolling back transaction")
        if conn:
            conn.rollback()
        print("Transaction rolled back successfully")
        return None

    finally:
        if cursor:
            cursor.close()


def test_vegetarian_pizza_constraint(conn):
    print("\n TESTING VEGETARIAN/VEGAN PIZZA CONSTRAINT")
    print("=" * 50)

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT pizza_id, name 
            FROM Pizza 
            WHERE is_vegetarian = TRUE 
            LIMIT 1
        """)
        vegetarian_pizza = cursor.fetchone()

        if not vegetarian_pizza:
            print("❌ No vegetarian pizzas found for testing")
            return False

        cursor.execute("""
            SELECT ingredient_id, name 
            FROM Ingredient 
            WHERE vegetarian = FALSE 
            LIMIT 1
        """)
        non_veg_ingredient = cursor.fetchone()

        if not non_veg_ingredient:
            print("❌ No non-vegetarian ingredients found for testing")
            return False

        print(
            f"Testing: Add non-vegetarian '{non_veg_ingredient['name']}' to vegetarian pizza '{vegetarian_pizza['name']}'")

        cursor.execute("""
            INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
            VALUES (%s, %s, 1.0)
        """, (vegetarian_pizza['pizza_id'], non_veg_ingredient['ingredient_id']))

        conn.commit()
        print("!!!CONSTRAINT FAILED: Should not allow non vegetarian ingredients in vegetarian pizza")
        return False

    except mysql.connector.Error as e:
        conn.rollback()
        print(f"CONSTRAINT WORKING: {e}")
        return True
    finally:
        cursor.close()


def test_discount_code_reuse(conn):
    print("\n TESTING DISCOUNT CODE REUSE CONSTRAINT")
    print("=" * 50)

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT dr.discount_id, dr.order_id, dr.customer_id
            FROM DiscountRedemption dr
            LIMIT 1
        """)
        used_discount = cursor.fetchone()

        if not used_discount:
            print("No used discount codes found, testing with new scenario")
            #Create test case
            cursor.execute("""
                INSERT INTO DiscountCode (discount_code, discount_value, discount_type, is_active)
                VALUES ('TEST_REUSE', 10, 'value', TRUE)
            """)
            discount_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO DiscountRedemption (discount_id, customer_id, order_id)
                VALUES (%s, 1, 1)
            """, (discount_id,))

            used_discount = {'discount_id': discount_id, 'order_id': 1, 'customer_id': 1}

        print(f"Testing: Reuse discount code #{used_discount['discount_id']} for order #{used_discount['order_id']}")

        cursor.execute("""
            INSERT INTO DiscountRedemption (discount_id, customer_id, order_id)
            VALUES (%s, %s, %s)
        """, (used_discount['discount_id'], used_discount['customer_id'], used_discount['order_id']))

        conn.commit()
        print("!!!CONSTRAINT FAILED: Should not allow discount code reuse for same order")
        return False

    except mysql.connector.Error as e:
        conn.rollback()
        print(f"CONSTRAINT WORKING: {e}")
        return True
    finally:
        cursor.close()


def test_negative_ingredient_price(conn):
    print("\nTESTING NEGATIVE INGREDIENT PRICE CONSTRAINT")
    print("=" * 50)

    cursor = conn.cursor(dictionary=True)

    try:
        print("Test - Insert ingredient with negative price")

        cursor.execute("""
            INSERT INTO Ingredient (name, price_per_unit, vegan, vegetarian, allergen)
            VALUES ('Test Negative Price Ingredient', -5.00, TRUE, TRUE, FALSE)
        """)

        conn.commit()
        print("!!!CONSTRAINT FAILED: Should not allow negative ingredient prices")
        return False

    except mysql.connector.Error as e:
        conn.rollback()
        print(f"CONSTRAINT HOLDS: {e}")
        return True
    finally:
        cursor.close()


def test_zero_pizza_price(conn):
    print("\nTESTING ZERO PIZZA PRICE CONSTRAINT")
    print("=" * 50)

    cursor = conn.cursor(dictionary=True)

    try:
        print("Testing: Insert pizza with zero base price")

        cursor.execute("""
            INSERT INTO Pizza (name, size, base_price, availability)
            VALUES ('Test Zero Price Pizza', 'M', 0.00, TRUE)
        """)

        conn.commit()
        print("!!!CONSTRAINT FAILED: Should not allow zero pizza prices")
        return False

    except mysql.connector.Error as e:
        conn.rollback()
        print(f"CONSTRAINT WORKING: {e}")
        return True
    finally:
        cursor.close()

def get_top_selling_pizzas(conn):
    try:
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            p.name AS pizza_name,
            p.size,
            SUM(oi.pizza_quantity) AS total_sold,
            SUM(oi.pizza_quantity * p.base_price) AS total_revenue
        FROM Pizza p
        JOIN OrderItem oi ON p.pizza_id = oi.pizza_id
        JOIN `Order` o ON oi.order_id = o.order_id
        WHERE o.status != 'cancelled'
        GROUP BY p.pizza_id, p.name, p.size
        ORDER BY total_sold DESC;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        print("\nTOP SELLING PIZZAS")
        print("=" * 50)
        for row in results:
            print(f"{row['pizza_name']} ({row['size']}): {row['total_sold']} sold, Revenue: {row['total_revenue']} EUR")

        return results



    except mysql.connector.Error as e:
        print(f"Error retrieving top selling pizzas: {e}")
        return []



if __name__ == "__main__":
    conn = create_connection()
    if conn:
        run_sql_file(conn, "insert_sample_data.sql")

        create_pizza_price_view(conn)

        retrieve_menu_data(conn)

        print("\n Analyzing sales data...")
        get_top_selling_pizzas(conn)

        get_undelivered_orders(conn)
        get_delivery_earnings_by_gender(conn)
        get_delivery_earnings_by_age(conn)
        get_delivery_earnings_by_postal_code(conn)

        test_vegetarian_pizza_constraint(conn)
        test_discount_code_reuse(conn)
        test_negative_ingredient_price(conn)
        conn.close()
