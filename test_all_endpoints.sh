#!/bin/bash
echo "=== ПОЛНОЕ ТЕСТИРОВАНИЕ API MES-X ==="
echo ""

# 1. Тестируем создание производственного задания
echo "1. 📋 Создаем производственное задание..."
curl -s -X POST "http://localhost:8000/api/v1/mo?order_number=MO001&product_name=Деталь%20А&product_code=DET-A&quantity=5"
echo -e "\n"

# 2. Тестируем создание операции
echo "2. ⚙️ Создаем операцию..."
curl -s -X POST "http://localhost:8000/api/v1/operations?manufacturing_order_id=1&operation_number=OP001&name=Фрезеровка&description=Черновая%20обработка"
echo -e "\n"

# 3. Тестируем создание заказа
echo "3. 📦 Создаем заказ..."
curl -s -X POST "http://localhost:8000/api/v1/orders?product_name=Изделие%20Б&quantity=10"
echo -e "\n"

# 4. Тестируем создание проекта
echo "4. 🗂️ Создаем проект..."
curl -s -X POST "http://localhost:8000/api/v1/projects?name=Проект%202&description=Новый%20проект"
echo -e "\n"

# 5. Тестируем создание сотрудника
echo "5. 👨‍💼 Создаем сотрудника..."
curl -s -X POST "http://localhost:8000/api/v1/employees?first_name=Алексей&last_name=Смирнов&role=Технолог"
echo -e "\n"

# 6. Тестируем запуск операции
echo "6. 🚀 Запускаем операцию..."
curl -s -X POST "http://localhost:8000/api/v1/operations/start?operation_id=1&employee_id=1"
echo -e "\n"

# 7. Тестируем регистрацию брака
echo "7. ⚠️ Регистрируем брак..."
curl -s -X POST "http://localhost:8000/api/v1/defects?operation_id=1&description=Тестовый%20брак&defect_type=качество"
echo -e "\n"

# 8. Тестируем получение QR кода
echo "8. 📱 Получаем QR код заказа..."
curl -s -X GET "http://localhost:8000/api/v1/qr/order/1"
echo -e "\n"

echo "=== ПРОВЕРКА GET ЗАПРОСОВ ==="
echo ""

# 9-14. Тестируем все GET эндпоинты
endpoints=(
    "Заказы:/api/v1/orders"
    "Проекты:/api/v1/projects" 
    "Операции:/api/v1/operations"
    "Сотрудники:/api/v1/employees"
    "Производственные задания:/api/v1/mo"
    "Браки:/api/v1/defects"
)

for endpoint in "${endpoints[@]}"; do
    IFS=':' read -r name path <<< "$endpoint"
    echo "📊 $name:"
    curl -s -X GET "http://localhost:8000$path" | python -m json.tool
    echo ""
done

echo "✅ Все тесты завершены!"
