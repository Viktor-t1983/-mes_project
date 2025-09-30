#!/bin/bash
echo "=== ПОЛНОЕ ТЕСТИРОВАНИЕ API MES-X ==="
echo ""

# 1. Создаем производственное задание
echo "1. 📋 Создаем производственное задание..."
curl -X POST "http://localhost:8000/api/v1/mo?order_number=MO001&product_name=Деталь%20А&product_code=DET-A&quantity=5"
echo -e "\n"

# 2. Создаем операцию
echo "2. ⚙️ Создаем операцию..."
curl -X POST "http://localhost:8000/api/v1/operations?manufacturing_order_id=1&operation_number=OP001&name=Фрезеровка&description=Черновая%20обработка"
echo -e "\n"

# 3. Создаем заказ
echo "3. 📦 Создаем заказ..."
curl -X POST "http://localhost:8000/api/v1/orders?product_name=Изделие%20Б&quantity=10"
echo -e "\n"

# 4. Создаем проект
echo "4. 🗂️ Создаем проект..."
curl -X POST "http://localhost:8000/api/v1/projects?name=Проект%202&description=Новый%20проект"
echo -e "\n"

# 5. Создаем сотрудника
echo "5. 👨‍💼 Создаем сотрудника..."
curl -X POST "http://localhost:8000/api/v1/employees?first_name=Алексей&last_name=Смирнов&role=Технолог"
echo -e "\n"

# 6. Запускаем операцию
echo "6. 🚀 Запускаем операцию..."
curl -X POST "http://localhost:8000/api/v1/operations/start?operation_id=1&employee_id=1"
echo -e "\n"

# 7. Регистрируем брак
echo "7. ⚠️ Регистрируем брак..."
curl -X POST "http://localhost:8000/api/v1/defects?operation_id=1&description=Тестовый%20брак&defect_type=качество"
echo -e "\n"

# 8. Получаем QR код
echo "8. 📱 Получаем QR код заказа..."
curl -X GET "http://localhost:8000/api/v1/qr/order/1"
echo -e "\n"

echo "=== ПРОВЕРКА ВСЕХ ДАННЫХ ==="
echo ""

echo "📊 Производственные задания:"
curl -s -X GET "http://localhost:8000/api/v1/mo" | python -m json.tool
echo ""

echo "📊 Операции:"
curl -s -X GET "http://localhost:8000/api/v1/operations" | python -m json.tool
echo ""

echo "📊 Заказы:"
curl -s -X GET "http://localhost:8000/api/v1/orders" | python -m json.tool
echo ""

echo "📊 Проекты:"
curl -s -X GET "http://localhost:8000/api/v1/projects" | python -m json.tool
echo ""

echo "📊 Сотрудники:"
curl -s -X GET "http://localhost:8000/api/v1/employees" | python -m json.tool
echo ""

echo "📊 Браки:"
curl -s -X GET "http://localhost:8000/api/v1/defects" | python -m json.tool
echo ""

echo "✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!"
