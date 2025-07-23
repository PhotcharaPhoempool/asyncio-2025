import asyncio
import httpx
import time

API_URL = "https://pokeapi.co/api/v2/ability/?limit=100"

async def fetch_ability_details(client, url):
    resp = await client.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data["name"], len(data["pokemon"])

async def main():
    async with httpx.AsyncClient() as client:
        resp = await client.get(API_URL)
        resp.raise_for_status()
        abilities = resp.json()["results"]
        tasks = [fetch_ability_details(client, ab["url"]) for ab in abilities]
        results = await asyncio.gather(*tasks)
        for name, count in results:
            print(f"{name} -> {count} pokemon")

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"Total time: {round(end - start, 2)} seconds")