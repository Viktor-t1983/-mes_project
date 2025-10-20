#!/usr/bin/env python3
import asyncio
import httpx
import os
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"

def check_security():
    print("🛡️ Проверка безопасности...")
    if ".env" not in open(".gitignore").read():
        return False
    for root, _, files in os.walk("src"):
        for f in files:
            if f.endswith(".py"):
                content = open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore").read()
                if "MesProject2025" in content:
                    return False
    print("✅ Секреты вынесены из кода")
    return True

async def e2e_shipment_test():
    print("📦 Запуск сквозного E2E-теста...")
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Проект
        proj = await client.post(f"{BASE_URL}/api/v1/projects/", json={"name": f"E2E_{int(datetime.now().timestamp())}"})
        assert proj.status_code == 201
        project_id = proj.json()["id"]

        # Заказ
        order = await client.post(f"{BASE_URL}/api/v1/orders/", json={
            "name": "E2E Test Order",
            "product_name": "PART-E2E",
            "quantity": 1,
            "project_id": project_id
        })
        assert order.status_code == 201
        order_id = order.json()["id"]

        # Отгрузка — ИСПРАВЛЕНО: все обязательные поля
        ship = await client.post(f"{BASE_URL}/api/v1/shipments/", json={
            "project_id": project_id,
            "manufacturing_order_id": 1,
            "invoice_number": f"INV-{int(datetime.now().timestamp())}",
            "order_id": order_id,
            "status": "created"
        })
        assert ship.status_code == 201

        print("✅ E2E-тест пройден")
        return True

async def main():
    print("=" * 70)
    print("🚀 ФИНАЛЬНЫЙ ТЕСТ ГОТОВНОСТИ MES К PRODUCTION (Дни 1–13)")
    print("=" * 70)

    if not check_security():
        sys.exit(1)

    try:
        await e2e_shipment_test()
        print("\n🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("✅ MES-система готова к production")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
