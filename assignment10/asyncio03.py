from random import random
import asyncio
import time


# coroutine to generate work
async def producer(queue: asyncio.Queue):
    print(f"{time.ctime()} Producer: Running")
    # generate work
    for _ in range(10):
        # generate a value
        value = random()            # 0.0–1.0
        # block to simulate work
        await asyncio.sleep(value)  # ใช้ค่าเดียวกับงานที่ consumer จะประมวลผล
        # add to the queue
        await queue.put(value)
    print(f"{time.ctime()} Producer: Done")


# coroutine to consume work
async def consumer(queue: asyncio.Queue):
    print(f"{time.ctime()} Consumer: Running")
    # consume work
    try:
        while True:
            # get a unit of work
            item = await queue.get()
            # report
            print(f"{time.ctime()} -> get {item:.3f}")
            # block while processing
            if item:
                await asyncio.sleep(item)
            # mark the task as done
            queue.task_done()
    except asyncio.CancelledError:
        # ออกจากลูปเมื่อถูกยกเลิกจาก main()
        print(f"{time.ctime()} Consumer: Cancelled")
        raise


# entry point coroutine
async def main():
    # create the shared queue
    queue = asyncio.Queue()

    # start the consumer
    consumer_task = asyncio.create_task(consumer(queue))

    # start producer and wait for it to finish
    await asyncio.create_task(producer(queue))

    # wait for all items to be processed
    await queue.join()

    # stop consumer gracefully
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass

    print(f"{time.ctime()} Main: All done")


asyncio.run(main())
