# example of using an asyncio queue without blocking
from random import random
import asyncio

# coroutine to generate work
async def producer(queue: asyncio.Queue):
    print('Producer: Running')
    # generate work
    for i in range(10):
        value = i
        sleeptime = random()
        print(f"> Producer {value} sleep {sleeptime:.2f}")
        await asyncio.sleep(sleeptime)  # simulate producing time
        print(f"> Producer put {value}")
        await queue.put(value)
    # send an all-done signal
    await queue.put(None)
    print('Producer: Done')

# coroutine to consume work (non-blocking poll)
async def consumer(queue: asyncio.Queue):
    print('Consumer: Running')
    while True:
        try:
            # get a unit of work without blocking
            item = queue.get_nowait()
        except asyncio.QueueEmpty:
            print("Consumer: got nothing, waiting a while...")
            await asyncio.sleep(0.5)
            continue

        # check for stop signal
        if item is None:
            break

        # report
        print(f"\t> Consumer got {item}")
        # (optional) simulate processing time
        await asyncio.sleep(0.1)

    print('Consumer: Done')

# entry point coroutine
async def main():
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue), consumer(queue))

asyncio.run(main())
