# Create 2 Tasks with High-Level API
import asyncio

async def download_image(name, delay):
    print(f"{name} downloading...")
    await asyncio.sleep(delay)
    print(f"{name} download complete!")

async def main():
    # create 2 tasks
    task1 = asyncio.create_task(download_image("img 1", 2))
    task2 = asyncio.create_task(download_image("img 2", 3))

    # wait for both task finish
    await task1
    await task2

asyncio.run(main())