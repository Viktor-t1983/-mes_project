#!/usr/bin/env python3
"""End-to-end тест: проект → MO → отгрузка"""
import asyncio
import httpx
import time

async def main():
    base = "http://localhost:8000"
    async with httpx.AsyncClient() as client:
        # 1. Создаём проект с уникальным именем
        project_name = f"E2E_Project_{int(time.time())}"
        project = await client.post(f"{base}/api/v1/projects/", json={
            "name": project_name,
            "status": "active"
        })
        assert project.status_code == 201, f"Project failed: {project.status_code} {project.text}"
        project_id = project.json()["id"]
        print(f"✅ Проект создан: id={project_id}")

        # 2. Создаём производственный заказ (MO)
        mo = await client.post(f"{base}/api/v1/manufacturing-orders/", json={
            "project_id": project_id,
            "part_number": "PART-E2E",
            "status": "completed"
        })
        assert mo.status_code == 201, f"MO failed: {mo.status_code} {mo.text}"
        mo_id = mo.json()["id"]
        print(f"✅ MO создан: id={mo_id}")

        # 3. Создаём отгрузку
        shipment = await client.post(f"{base}/api/v1/shipments/", json={
            "project_id": project_id,
            "manufacturing_order_id": mo_id,
            "invoice_number": "E2E-INV-001"
        })
        assert shipment.status_code == 201, f"Shipment create failed: {shipment.status_code} {shipment.text}"
        shipment_id = shipment.json()["id"]
        print(f"✅ Отгрузка создана: id={shipment_id}")

        # 4. Подтверждаем кладовщиком
        confirm_warehouse = await client.post(f"{base}/api/v1/shipments/{shipment_id}/confirm-warehouse", json={"employee_qr": "WH_001"})
        assert confirm_warehouse.status_code == 200
        print("✅ Отгрузка подтверждена кладовщиком")

        # 5. Подтверждаем экспедитором
        confirm_transporter = await client.post(f"{base}/api/v1/shipments/{shipment_id}/confirm-transporter", json={"transporter_qr": "TR_001", "tracking_number": "E2E-TRACK"})
        assert confirm_transporter.status_code == 200
        print("✅ Отгрузка завершена экспедитором")

        print("\n🎉 E2E ТЕСТ УСПЕШЕН")

if __name__ == "__main__":
    asyncio.run(main())
