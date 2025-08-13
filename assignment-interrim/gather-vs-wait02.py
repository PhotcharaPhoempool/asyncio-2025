import asyncio, time

async def worker_error():
    print(f'{time.ctime()} [Worker error]: Start')
    await asyncio.sleep(1)
    raise ValueError("Boom!")

async def main():
    asyncio.create_task(worker_error())
    await asyncio.sleep(2)

asyncio.run(main())