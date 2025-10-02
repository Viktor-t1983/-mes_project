#!/bin/bash
echo "💾 Резервное копирование БД MES..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U postgres mes_db > backups/mes_backup_${TIMESTAMP}.sql
echo "✅ Бэкап создан: backups/mes_backup_${TIMESTAMP}.sql"