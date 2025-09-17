from fastapi import FastAPI, HTTPException
import asyncio
import random

app = FastAPI(title="Asynchronous Rocket Launcher")

rockets = []

async def launch_rocket(student_id: str, delay: float):
    print(f"Rocket {student_id} launched! ETA: {delay:.2f} seconds")
    await asyncio.sleep(delay)
    print(f"Rocket {student_id} reached destination after {delay:.2f} seconds")

@app.get("/fire/{student_id}")
async def fire_rocket(student_id: str):
    if len(student_id) != 10 or not student_id.isdigit():
        raise HTTPException(status_code=400, detail="student_id must be 10 digits")
    delay = round(random.uniform(1, 2), 2)
    task = asyncio.create_task(launch_rocket(student_id, delay))
    rockets.append(task)
    await asyncio.sleep(delay)
    return {
        "message": f"Rocket {student_id} fired!",
        "time_to_target": delay
    }
