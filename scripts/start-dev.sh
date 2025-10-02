#!/bin/bash
echo "🚀 Запуск MES Development..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000