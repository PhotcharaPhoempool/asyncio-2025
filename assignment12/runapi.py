import asyncio
import httpx
import json


# --------------------
# Config: server URLs
# --------------------
SERVERS = [
    "http://172.20.48.160:8000/",
    "http://172.20.49.54:8000/",
    "http://172.20.50.19:8000/",


]

ENDPOINTS = [
    "/students",
    "/analytics/group",
    "/analytics/year"
]

# --------------------
# Fetch single endpoint
# --------------------
async def fetch_endpoint(client, server, endpoint):
    try:
        resp = await client.get(f"{server}{endpoint}", timeout=5.0)
        resp.raise_for_status()
        data = resp.json()
        try:
            count = len(data)  # ถ้า data เป็น list/dict/str
        except TypeError:
            count = 1  # fallback สำหรับ data ที่ไม่สามารถ len() ได้
        return {"server": server, "endpoint": endpoint, "count": count}
    except Exception as e:
        return {"server": server, "endpoint": endpoint, "error": str(e)}

# --------------------
# Fetch all endpoints from one server concurrently
# --------------------
async def fetch_from_server(client: httpx.AsyncClient, server: str):
    tasks = [fetch_endpoint(client, server, ep) for ep in ENDPOINTS]
    return await asyncio.gather(tasks)

# --------------------
# Main
# --------------------
async def main():
    async with httpx.AsyncClient() as client:
        # ยิงทุก server พร้อมกัน
        tasks = [fetch_from_server(client, server) for server in SERVERS]
        all_results = await asyncio.gather(tasks)

        for server_results in all_results:
            for entry in server_results:
                print(json.dumps(entry, ensure_ascii=False, indent=2))

if __name__ == "main":
    asyncio.run(main())