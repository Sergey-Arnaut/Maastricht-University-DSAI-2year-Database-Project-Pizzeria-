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


if __name__ == "__main__":
    conn = create_connection()
    if conn:
        # 1. Загружаем тестовые данные из файла
        run_sql_file(conn, "insert_sample_data.sql")

        # 2. Создаем представление
        create_pizza_price_view(conn)

        # 3. Достаем меню
        retrieve_menu_data(conn)

        conn.close()
