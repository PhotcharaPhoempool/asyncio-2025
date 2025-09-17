import time
import asyncio
import httpx

student_id = "6610301008"

async def fire_rocket(name: str, t0: float):
    url = f"http://172.16.2.117:8088/fire/{student_id}"
    # url = f"http://127.0.0.1:8088/fire/{student_id}"
    start_time = time.perf_counter() - t0  # เวลาเริ่มสัมพัทธ์
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
        time_to_target = data.get("time_to_target", 0)
    end_time = time.perf_counter() - t0
    return {
        "name": name,
        "start_time": start_time,
        "time_to_target": time_to_target,
        "end_time": end_time
    }

async def main():
    t0 = time.perf_counter()  # เวลาเริ่มของชุด rockets

    print("Rocket prepare to launch ...")  # แสดงตอนเริ่ม main

    # สร้าง task ยิง rocket 3 ลูกพร้อมกัน
    tasks = [
        asyncio.create_task(fire_rocket(f"Rocket-{i+1}", t0))
        for i in range(3)
    ]

    # รอให้ทุก task เสร็จและเก็บผลลัพธ์ตามลำดับ task
    results = await asyncio.gather(*tasks)

    # เรียงลำดับ rocket ตามเวลาที่ถึงจุดหมาย
    results.sort(key=lambda r: r["end_time"])

    print("Rockets fired:")
    # แสดงผล start_time, time_to_target, end_time ของแต่ละ rocket ตามลำดับ task
    for r in results:
        print(f"{r['name']} | start_time: {r['start_time']:.2f} sec | time_to_target: {r['time_to_target']:.2f} sec | end_time: {r['end_time']:.2f} sec")

    # แสดงเวลารวมทั้งหมดตั้งแต่ยิงลูกแรกจนลูกสุดท้ายถึงจุดหมาย
    t_total = max(r["end_time"] for r in results)
    print(f"\nTotal time for all rockets: {t_total:.2f} sec")

if __name__ == "__main__":
    asyncio.run(main())
