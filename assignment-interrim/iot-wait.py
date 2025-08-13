import asyncio, time, random

async def get_temperature():
    await asyncio.sleep(random.uniform(0.5, 2.0))  # Simulate sensor reading delay
    return "Temp 30 °C"

async def get_humidity():
    await asyncio.sleep(random.uniform(0.5, 2.0))  # Simulate sensor reading delay
    return "Humidity 60%"

async def get_weather_api():
    await asyncio.sleep(random.uniform(0.5, 2.0))  # Simulate API call delay
    return "Weather: Sunny"

async def main():
    start = time.time()

    pending = {
        asyncio.create_task(get_humidity()),
        asyncio.create_task(get_temperature()),
        asyncio.create_task(get_weather_api()),
    }

    while pending:
        done, pending = await asyncio.wait(
            pending, return_when=asyncio.FIRST_COMPLETED
        )
        for d in done:
            try:
                result = d.result()
                print(f"• {time.ctime()} → {result}")
            except Exception as e:
                print(f"• {time.ctime()} → ERROR: {e}")

    print(f"\n• Took {time.time() - start:.2f} seconds")

asyncio.run(main())