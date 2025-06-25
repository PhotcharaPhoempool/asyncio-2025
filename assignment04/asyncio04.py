# example of starting many tasks and getting access to all tasks
import time
import asyncio

# Coroutine for a task
async def download_image(name, delay):
    print(f"{name} downloading...")
    await asyncio.sleep(delay)
    print(f"{name} download complete!")

# Define a main coroutine
async def main():
    # Report a message
    print(f'{time.ctime()} main coroutine started')
    # Start many tasks
    started_tasks = [asyncio.create_task(download_image(i, i)) for i in range(3)]
    # Allow some of the tasks time to start
    await asyncio.sleep(0.1)
    for task in started_tasks:
        await task

# start the asyncio program
asyncio.run(main())