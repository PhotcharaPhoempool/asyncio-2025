# Question
1. ถ้าสร้าง asyncio.create_task(*tasks) ที่ไม่มี await ที่ main() เกิดอะไรบ้าง
   1. เริ่มทำงานทันทีแบบเบื้องหลัง — task ถูก schedule ให้รันบน event loop แต่โค้ดหลักจะ ไม่รอ ให้เสร็จ
   2. อาจถูกยกเลิกตอนจบโปรแกรม — ถ้า main() จบและ asyncio.run() ปิด loop ขณะที่ยังมี task ค้างอยู่ งานนั้นจะถูกยกเลิก/ทำไม่เสร็จ และอาจเห็นคำเตือน “Task was destroyed but it is pending!”
   3. ข้อยกเว้นไม่ถูกส่งต่อให้ผู้เรียก — exception ภายใน task จะไม่เด้งมาที่ main() (มักไปโผล่เป็น warning “Task exception was never retrieved”) เว้นแต่คุณ await task นั้น หรือดักจับในตัว coroutine/ใส่ add_done_callback

2. ความแตกต่างระหว่าง asyncio.gather(*tasks) กับ asyncio.wait(tasks) คืออะไร
   1. การคืนค่า
      - gather → คืน ลิสต์ผลลัพธ์ เรียงตามลำดับพารามิเตอร์
      - wait → คืนคู่ (done, pending) เป็น ชุดของ task objects (ต้องไป t.result() เอง)
   2. การจัดการ error
      - gather (ค่าเริ่มต้น) → task ใดพังจะ raise ทันที และ ยกเลิก ที่เหลือ (ปรับได้ด้วย return_exceptions=True)
      - wait → ไม่ raise เอง; คุณเลือกไล่อ่านผล/จับข้อยกเว้นจากแต่ละ t.result() ได้ละเอียดกว่า
   3. รอเฉพาะงานแรกที่เสร็จ
      - gather → ไม่รองรับ ต้องรอครบทุกงาน
      - wait → รองรับ ผ่าน return_when=asyncio.FIRST_COMPLETED (หรือ FIRST_EXCEPTION, ALL_COMPLETED)

3. สร้าง create_task() และ coroutine ของ http ให้อะไรต่างกัน
   1. เวลาเริ่มรัน
      - create_task(http_coro()) → เริ่มรันทันที (background) แล้วค่อยไป await/จัดการภายหลัง
      - ส่ง coroutine ตรงให้ await/gather → จะเริ่มเมื่อถึงจุด await/gather เท่านั้น
   2. การควบคุมงานรายตัว
      - create_task มี handle ของ task → ยกเลิก, ใส่ timeout, ผูก callback, ติดตามสถานะ ได้สะดวก
      - coroutine ตรง ๆ → ควบคุมรายตัวได้จำกัด (มักใช้รอผลรวมทีเดียวด้วย gather)
   3. อายุทรัพยากร (สำคัญกับ HTTP client)
      - ถ้าใช้ create_task ภายใน async with httpx.AsyncClient()/aiohttp.ClientSession() ต้องแน่ใจว่า session ยังไม่ปิด จนกว่า task ทั้งหมดจะเสร็จ ไม่งั้นจะเจอ “Session is closed”
      - ใช้ await/gather ภายในบล็อก async with จะง่ายกว่าเพราะอายุ session ผูกกับช่วงรอผลพอดี
