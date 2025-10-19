import mysql.connector
import os

# Настройки подключения к БД
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
    """Создает соединение с базой данных"""
    try:
        conn = mysql.connector.connect(**db_config)
        print("✅ Successful connection to database!")
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Mistake with connection to MySQL: {e}")
        return None


def run_sql_file(conn, filename):
    """Запускает SQL-скрипт из файла"""
    try:
        cursor = conn.cursor()
        with open(filename, "r", encoding="utf-8") as f:
            sql_script = f.read()

        # Выполняем все команды по очереди
        for statement in sql_script.split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)

        conn.commit()
        print(f"✅ SQL file '{filename}' executed successfully!")

    except Exception as e:
        print(f"❌ Error executing SQL file '{filename}': {e}")


def create_pizza_price_view(conn):
    """Создает представление для расчета цен пицц"""
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
        print("✅ Pizza price view created successfully!")
        return True

    except mysql.connector.Error as e:
        print(f"❌ Error creating pizza price view: {e}")
        return False


def retrieve_menu_data(conn):
    """Извлекает данные меню из представления"""
    try:
        cursor = conn.cursor(dictionary=True)

        print("\n🍕 RETRIEVING MENU DATA")
        print("=" * 50)

        cursor.execute("SELECT * FROM PizzaPriceView;")
        rows = cursor.fetchall()

        for row in rows:
            print(f"{row['pizza_name']} ({row['size']}): {row['final_price']} EUR")

        return rows

    except mysql.connector.Error as e:
        print(f"❌ Error retrieving menu data: {e}")
        return []


def get_undelivered_orders(conn):
    """Получает не доставленные заказы"""
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

        print("\n🚫 UNDELIVERED ORDERS")
        print("=" * 60)

        if not results:
            print("✅ All orders have been delivered or cancelled!")
            return []

        for row in results:
            status_emoji = {
                'pending': '⏳',
                'preparing': '👨‍🍳',
                'baking': '🔥',
                'ready': '✅',
                'out_for_delivery': '🚗'
            }.get(row['status'], '❓')

            print(f"Order #{row['order_id']} {status_emoji}")
            print(f"   Customer: {row['first_name']} {row['last_name']}")
            print(f"   Status: {row['status']}")
            print(f"   Ordered: {row['order_timestamp']}")
            print(f"   Total: {row['total_price']} EUR")
            print(f"   Delivery to: {row['delivery_postal_code']}")
            print(f"   Pending for: {row['minutes_pending']} minutes")
            print("-" * 40)

        return results

    except mysql.connector.Error as e:
        print(f"❌ Error retrieving undelivered orders: {e}")
        return []
def get_delivery_earnings_by_gender(conn):
    """Анализ заработков доставщиков по полу"""
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
        print(f"❌ Error retrieving earnings by gender: {e}")
        return []
def get_delivery_earnings_by_age(conn):
    """Анализ заработков доставщиков по возрасту"""
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
    """Анализ заработков доставщиков по почтовому индексу"""
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
def get_top_selling_pizzas(conn):
    """Получает самые продаваемые пиццы"""
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

        print("\n🏆 TOP SELLING PIZZAS")
        print("=" * 50)
        for row in results:
            print(f"{row['pizza_name']} ({row['size']}): {row['total_sold']} sold, Revenue: {row['total_revenue']} EUR")

        return results



    except mysql.connector.Error as e:
        print(f"❌ Error retrieving top selling pizzas: {e}")
        return []



if __name__ == "__main__":
    conn = create_connection()
    if conn:
        # 1. Загружаем тестовые данные из файла
        run_sql_file(conn, "insert_sample_data.sql")

        # 2. Создаем представление
        create_pizza_price_view(conn)

        # 3. Достаем меню
        retrieve_menu_data(conn)

        #4 top seller pizzas
        print("\n Analyzing sales data...")
        get_top_selling_pizzas(conn)

        #5 undelivered orders
        get_undelivered_orders(conn)
        #6 salary stats
        get_delivery_earnings_by_gender(conn)
        get_delivery_earnings_by_age(conn)
        get_delivery_earnings_by_postal_code(conn)
        conn.close()
