import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def add_test_data():
    db_url = os.getenv("DATABASE_URL")
    if "asyncpg" in db_url:
        db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    
    print("📝 ДОБАВЛЕНИЕ ТЕСТОВЫХ ДАННЫХ")
    print("=" * 35)
    
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Проверяем есть ли данные в orders
        cursor.execute("SELECT COUNT(*) FROM orders")
        orders_count = cursor.fetchone()[0]
        
        if orders_count == 0:
            print("📝 Добавляем тестовые данные в orders...")
            cursor.execute("""
                INSERT INTO orders (project_id, name, description, product_name, quantity, status) VALUES
                (1, 'Производственный заказ 001', 'Основной заказ на производство', 'Деталь А', 100, 'pending'),
                (1, 'Производственный заказ 002', 'Второй производственный заказ', 'Деталь Б', 50, 'in_progress'),
                (1, 'Тестовый заказ 003', 'Заказ для тестирования системы', 'Тестовая деталь', 10, 'completed')
            """)
            print(f"✅ Добавлено записей в orders: {cursor.rowcount}")
        
        # Проверяем есть ли данные в operations
        cursor.execute("SELECT COUNT(*) FROM operations")
        operations_count = cursor.fetchone()[0]
        
        if operations_count == 0:
            print("📝 Добавляем тестовые данные в operations...")
            cursor.execute("""
                INSERT INTO operations (manufacturing_order_id, operation_number, name, description, 
                                      operation_type, workcenter_id, planned_duration, actual_duration, status) VALUES
                (1, 'OP001', 'Фрезеровка', 'Основная операция фрезеровки', 'production', 1, 120.5, 115.2, 'completed'),
                (1, 'OP002', 'Шлифовка', 'Финишная шлифовка поверхности', 'production', 1, 60.0, 55.5, 'completed'),
                (2, 'OP001', 'Сборка', 'Основная сборка компонентов', 'assembly', 2, 180.0, NULL, 'in_progress')
            """)
            print(f"✅ Добавлено записей в operations: {cursor.rowcount}")
        
        # Проверяем есть ли данные в employees
        cursor.execute("SELECT COUNT(*) FROM employees")
        employees_count = cursor.fetchone()[0]
        
        if employees_count == 0:
            print("📝 Добавляем тестовые данные в employees...")
            cursor.execute("""
                INSERT INTO employees (qr_code, first_name, last_name, role, allowed_workcenters, is_active) VALUES
                ('EMP001', 'Иван', 'Иванов', 'operator', '["wc1", "wc2"]', true),
                ('EMP002', 'Петр', 'Петров', 'supervisor', '["wc1", "wc2", "wc3"]', true),
                ('EMP003', 'Мария', 'Сидорова', 'quality', '["qc1"]', true)
            """)
            print(f"✅ Добавлено записей в employees: {cursor.rowcount}")
        
        # Проверяем есть ли данные в projects
        cursor.execute("SELECT COUNT(*) FROM projects")
        projects_count = cursor.fetchone()[0]
        
        if projects_count == 0:
            print("📝 Добавляем тестовые данные в projects...")
            cursor.execute("""
                INSERT INTO projects (name, description, status) VALUES
                ('Основной проект', 'Главный производственный проект', 'active'),
                ('Тестовый проект', 'Проект для тестирования системы', 'active')
            """)
            print(f"✅ Добавлено записей в projects: {cursor.rowcount}")
        
        print("\n🎉 ТЕСТОВЫЕ ДАННЫЕ ДОБАВЛЕНЫ!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    add_test_data()
