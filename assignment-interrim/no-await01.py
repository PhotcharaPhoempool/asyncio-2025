import asyncio, time

async def worker_ok():
    print(f'{time.ctime()} Worker OK: Start')
    await asyncio.sleep(1)
    print(f'{time.ctime()} Worker OK: Done')

async def main():
    asyncio.create_task(worker_ok())
    await asyncio.sleep(2)

asyncio.run(main())