import asyncio, time

async def worker_long():
    print(f'{time.ctime()} [Worker Long]: Start')
    try:
        await asyncio.sleep(5)
        print(f'{time.ctime()} [Worker Long]: Done')
    except asyncio.CancelledError:
        print(f'{time.ctime()} [Worker Long]: Cancelled!')

async def main():
    print(f'{time.ctime()} Starting main loop...')
    asyncio.create_task(worker_long())
    await asyncio.sleep(1)
    print(f'{time.ctime()} Main loop finished...!')

asyncio.run(main())