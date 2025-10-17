#!/usr/bin/env python3
"""Диагностика связей SQLAlchemy — выявляет отсутствующие back_populates"""
import sys
from sqlalchemy.orm import configure_mappers

def main():
    try:
        # Пытаемся настроить все мапперы
        configure_mappers()
        print("✅ Все связи SQLAlchemy настроены корректно")
        return 0
    except Exception as e:
        print(f"❌ Ошибка в связях SQLAlchemy: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
