#!/bin/bash
if [ -z "$1" ]; then
  echo "❌ Usage: $0 <backup_file.sql>"
  exit 1
fi

echo "🔄 Восстановление БД из $1..."
psql -h localhost -U postgres mes_db < "$1"
echo "✅ Восстановление завершено."
