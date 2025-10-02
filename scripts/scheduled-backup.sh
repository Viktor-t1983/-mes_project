#!/bin/bash
# Scheduled Backup Script for Cron
set -euo pipefail

TIMESTAMP=20251002_234524
BACKUP_FILE="backups/mes_backup_.sql"

echo "Thu Oct  2 23:45:24     2025: Starting scheduled backup" >> backups/backup.log
pg_dump  > ""

# Keep only last 7 daily backups
find backups/ -name "mes_backup_*.sql" -mtime +7 -delete

echo "Thu Oct  2 23:45:25     2025: Backup completed: " >> backups/backup.log
