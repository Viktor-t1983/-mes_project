import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    print("🗄️ СОЗДАНИЕ ТАБЛИЦ В БАЗЕ ДАННЫХ")
    print("=" * 50)
    
    try:
        # Подключаемся к базе
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres", 
            password="MesProject2025",
            database="mes_db"
        )
        cursor = conn.cursor()
        
        print("✅ Подключение к базе установлено")
        
        # SQL для создания таблиц
        tables_sql = [
            # Таблица сотрудников
            '''
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                role VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''',
            
            # Таблица заказов
            '''
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                status VARCHAR(50) DEFAULT 'новый',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''',
            
            # Таблица производственных заданий
            '''
            CREATE TABLE IF NOT EXISTS manufacturing_orders (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders(id),
                name VARCHAR(200) NOT NULL,
                status VARCHAR(50) DEFAULT 'активно',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''',
            
            # Таблица операций
            '''
            CREATE TABLE IF NOT EXISTS operations (
                id SERIAL PRIMARY KEY,
                manufacturing_order_id INTEGER REFERENCES manufacturing_orders(id),
                employee_id INTEGER REFERENCES employees(id),
                operation_type VARCHAR(100) NOT NULL,
                status VARCHAR(50) DEFAULT 'начата',
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''',
            
            # Таблица отчетов о дефектах
            '''
            CREATE TABLE IF NOT EXISTS defect_reports (
                id SERIAL PRIMARY KEY,
                manufacturing_order_id INTEGER REFERENCES manufacturing_orders(id),
                operation_id INTEGER REFERENCES operations(id),
                defect_type VARCHAR(100) NOT NULL,
                description TEXT,
                severity VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''',
            
            # Таблица проектов
            '''
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                status VARCHAR(50) DEFAULT 'активен',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
        ]
        
        # Создаем таблицы
        for i, sql in enumerate(tables_sql, 1):
            try:
                cursor.execute(sql)
                print(f"✅ Таблица {i} создана/проверена")
            except Exception as e:
                print(f"⚠️ Ошибка создания таблицы {i}: {e}")
        
        conn.commit()
        
        # Проверяем созданные таблицы
        cursor.execute('''
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        ''')
        
        tables = cursor.fetchall()
        print(f"\n📊 СОЗДАННЫЕ ТАБЛИЦЫ ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 БАЗА ДАННЫХ ГОТОВА К ИСПОЛЬЗОВАНИЮ!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}")
        return False

if __name__ == "__main__":
    create_tables()
