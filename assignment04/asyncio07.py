# get result
import asyncio

async def simple_task():
    await asyncio.sleep(1)
    return "Complete"

async def main():
    task = asyncio.create_task(simple_task())
    await task
    print("Result of task:", task.result())

asyncio.run(main())