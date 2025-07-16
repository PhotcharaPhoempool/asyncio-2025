import asyncio
import httpx
import time

names = [
    "pikachu", "bulbasaur", "charmander", "squirtle", "eevee",
    "snorlax", "gengar", "mewtwo", "psyduck", "jigglypuff"
]

API_URL = "https://pokeapi.co/api/v2/pokemon/{}"

async def fetch_pokemon(client, name):
    url = API_URL.format(name)
    resp = await client.get(url)
    resp.raise_for_status()
    data = resp.json()
    return {
        "name": data["name"].capitalize(),
        "id": data["id"],
        "base_experience": data["base_experience"]
    }

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch_pokemon(client, name) for name in names]
        results = await asyncio.gather(*tasks)
        sorted_results = sorted(results, key=lambda x: x["base_experience"], reverse=True)
        print(f"{'Name':<12} {'ID':<4} {'Base Experience':<16}")
        print("-" * 34)
        for p in sorted_results:
            print(f"{p['name']:<12} {p['id']:<4} {p['base_experience']:<16}")

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"Total time: {round(end - start, 2)} seconds")