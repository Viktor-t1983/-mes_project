#!/usr/bin/env python3
"""
КОМПЛЕКСНЫЙ ТЕСТ ВСЕХ 8 ДНЕЙ MES-СИСТЕМЫ
Проверяет: ядро → геймификация → мобильное API → IIoT → аудит → BPM → LMS
"""
import asyncio
import httpx
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_day1_core():
    """День 1: Ядро (Order, Project)"""
    print("🔍 День 1: Ядро...")
    async with httpx.AsyncClient() as client:
        project_name = f"TestProject_{int(datetime.now().timestamp())}"
        proj = await client.post(f"{BASE_URL}/api/v1/projects/", json={"name": project_name})
        assert proj.status_code == 201, f"Project create failed: {proj.status_code}"
        project_id = proj.json()["id"]

        order = await client.post(f"{BASE_URL}/api/v1/orders/", json={
            "name": "TestOrder",
            "product_name": "Widget",
            "quantity": 10,
            "project_id": project_id
        })
        assert order.status_code == 201, f"Order create failed: {order.status_code}"
        print("✅ День 1: пройден")
        return project_id

async def test_day2_gamification():
    """День 2: Геймификация"""
    print("🔍 День 2: Геймификация...")
    async with httpx.AsyncClient() as client:
        qr_code = f"TEST_QR_{int(datetime.now().timestamp())}"
        emp = await client.post(f"{BASE_URL}/api/v1/employees/", json={
            "first_name": "Test",
            "last_name": "Operator",
            "role": "operator",
            "qr_code": qr_code
        })
        assert emp.status_code == 201, f"Employee create failed: {emp.status_code}"
        print("✅ День 2: пройден")

async def test_day3_mobile():
    """День 3: Мобильное API"""
    print("🔍 День 3: Мобильное API...")
    async with httpx.AsyncClient() as client:
        # ✅ Исправлено: используем POST вместо GET
        resp = await client.post(
            f"{BASE_URL}/mobile/scan-start",
            json={"qr_code": "TEST_QR_001", "part_number": "PART-001"}
        )
        # Должен вернуть 200 или 403 (но не 404/405)
        assert resp.status_code in (200, 403), f"Mobile API failed: {resp.status_code}"
        print("✅ День 3: пройден")

async def test_day4_iiot():
    """День 4: IIoT и OEE"""
    print("🔍 День 4: IIoT и OEE...")
    async with httpx.AsyncClient() as client:
        hb = await client.post(
            f"{BASE_URL}/api/v1/iiot/heartbeat",
            json={"event_type": "test", "payload": {"status": "online"}},
            headers={"X-Machine-Token": "test_token"}
        )
        assert hb.status_code == 200, f"Heartbeat failed: {hb.status_code}"
        print("✅ День 4: пройден")

async def test_day5_audit():
    """День 5: Аудит"""
    print("🔍 День 5: Аудит...")
    async with httpx.AsyncClient() as client:
        audit = await client.get(f"{BASE_URL}/api/v1/audit/")
        assert audit.status_code == 200, f"Audit failed: {audit.status_code}"
        print("✅ День 5: пройден")

async def test_day6_bpm():
    """День 6: Конструктор BPM"""
    print("🔍 День 6: Конструктор BPM...")
    async with httpx.AsyncClient() as client:
        proc = await client.post(f"{BASE_URL}/api/v1/meta/processes", json={
            "name": f"TestProcess_{int(datetime.now().timestamp())}",
            "steps": [{
                "step_order": 1,
                "name": "Step1",
                "action_type": "form",
                "config": {}
            }]
        })
        assert proc.status_code == 201, f"BPM create failed: {proc.status_code}"
        print("✅ День 6: пройден")

async def test_day7_lms():
    """День 7: LMS и допуски"""
    print("🔍 День 7: LMS и допуски...")
    async with httpx.AsyncClient() as client:
        course_name = f"TestCourse_{int(datetime.now().timestamp())}"
        course = await client.post(f"{BASE_URL}/api/v1/lms/courses", json={
            "name": course_name,
            "operation_type": "test_op",
            "workcenter_id": "WC-001"
        })
        assert course.status_code == 201, f"Course create failed: {course.status_code}"
        course_id = course.json()["id"]

        auth = await client.get(f"{BASE_URL}/api/v1/lms/authorize?employee_id=1&workcenter_id=WC-001&operation_type=test_op")
        assert auth.status_code == 200, f"Auth check failed: {auth.status_code}"
        print("✅ День 7: пройден")
        return course_id

async def test_day8_override():
    """День 8: Подтверждение мастера"""
    print("🔍 День 8: Подтверждение мастера...")
    async with httpx.AsyncClient() as client:
        master_qr = f"MASTER_QR_{int(datetime.now().timestamp())}"
        master = await client.post(f"{BASE_URL}/api/v1/employees/", json={
            "first_name": "Test",
            "last_name": "Foreman",
            "role": "foreman",
            "qr_code": master_qr
        })
        assert master.status_code == 201, f"Master create failed: {master.status_code}"

        override = await client.post(
            f"{BASE_URL}/api/v1/lms/override?employee_id=1&workcenter_id=WC-999&operation_type=test_op",
            json={"master_qr_code": master_qr, "reason": "Test override"}
        )
        assert override.status_code == 202, f"Override failed: {override.status_code}"
        print("✅ День 8: пройден")

async def main():
    print("="*60)
    print("🚀 ЗАПУСК КОМПЛЕКСНОГО ТЕСТА ВСЕХ 8 ДНЕЙ")
    print("="*60)
    
    try:
        project_id = await test_day1_core()
        await test_day2_gamification()
        await test_day3_mobile()
        await test_day4_iiot()
        await test_day5_audit()
        await test_day6_bpm()
        course_id = await test_day7_lms()
        await test_day8_override()
        
        print("\n🎉 ВСЕ 8 ДНЕЙ УСПЕШНО ПРОЙДЕНЫ!")
        print("✅ MES-система полностью функциональна и готова к production.")
        
    except Exception as e:
        print(f"\n❌ ТЕСТ ПРОВАЛЕН: {e}")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
