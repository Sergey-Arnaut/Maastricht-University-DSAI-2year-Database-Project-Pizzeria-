import mysql.connector
import os

# Settings needed for connection to db
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


def run_simple_select_query(conn):
    """Выполняет простой SELECT запрос для проверки соединения"""
    try:
        cursor = conn.cursor()

        # Простой запрос для проверки соединения
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        print(f"✅ Simple SELECT query executed successfully! Result: {result[0]}")
        return True

    except mysql.connector.Error as e:
        print(f"❌ Error executing SELECT query: {e}")
        return False


def check_database_tables(conn):
    """Проверяет существование таблиц в базе данных"""
    try:
        cursor = conn.cursor()

        # Получаем список всех таблиц в базе данных
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print("📊 Database tables:")
        if tables:
            for table in tables:
                print(f"   ✅ {table[0]}")
            return True
        else:
            print("   ❌ No tables found in database")
            return False

    except mysql.connector.Error as e:
        print(f"❌ Error checking database tables: {e}")
        return False


def test_connection_and_queries():
    """Тестирует соединение и выполняет простые запросы"""
    print("🚀 Testing database connection and queries...")
    print("=" * 50)

    # Создаем соединение
    conn = create_connection()
    if not conn:
        return False

    try:
        # Тест 1: Простой SELECT запрос
        print("\n1. 🔍 Running simple SELECT query...")
        if not run_simple_select_query(conn):
            return False

        # Тест 2: Проверка таблиц
        print("\n2. 📋 Checking database tables...")
        if not check_database_tables(conn):
            return False

        # Тест 3: Пример запроса к конкретной таблице (если таблицы существуют)
        print("\n3. 🍕 Sample data query (if tables exist)...")
        try:
            cursor = conn.cursor()
            # Пробуем получить данные из таблицы Pizza, если она существует
            cursor.execute("""
                SELECT COUNT(*) as table_exists 
                FROM information_schema.tables 
                WHERE table_schema = 'our_little_secret' 
                AND table_name = 'Pizza'
            """)
            pizza_table_exists = cursor.fetchone()[0] > 0

            if pizza_table_exists:
                cursor.execute("SELECT pizza_id, name, size FROM Pizza LIMIT 3")
                pizzas = cursor.fetchall()
                if pizzas:
                    print("   Sample pizzas:")
                    for pizza in pizzas:
                        print(f"     {pizza[0]}. {pizza[1]} ({pizza[2]})")
                else:
                    print("   No pizzas found in table")
            else:
                print("   Pizza table doesn't exist yet")

        except mysql.connector.Error as e:
            print(f"   ℹ️  Info: {e}")

        print("\n" + "=" * 50)
        print("🎉 All connection tests passed successfully!")
        print("✅ Database connection is working properly")
        print("✅ Simple SELECT queries can be executed")
        print("✅ Ready for application development")

        return True

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    finally:
        if conn:
            conn.close()
            print("\n🔌 Database connection closed.")


def main():
    """Основная функция"""
    print("🔌 DATABASE CONNECTION TEST")
    print("=" * 50)

    # Запускаем тесты
    success = test_connection_and_queries()

    if success:
        print("\n Week 2 criteria completed!")
        print("   - Database connection established")
        print("   - Simple SELECT queries executed")
        print("   - Ready for application development")
    else:
        print("\n❌ Connection test failed")


if __name__ == "__main__":
    main()
