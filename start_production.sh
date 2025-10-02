#!/bin/bash
echo "🚀 Запуск MES Day 4 Production System"
echo "======================================"

# Проверяем виртуальное окружение
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено"
    exit 1
fi

# Активируем venv
source venv/Scripts/activate

# Убиваем старые процессы
echo "🛑 Останавливаем старые процессы..."
pkill -f "python main.py" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true

# Запускаем сервер
echo "✅ Запускаем MES Day 4 сервер..."
python main.py
