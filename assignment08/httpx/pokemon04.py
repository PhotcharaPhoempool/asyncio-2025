import asyncio
import httpx
import time

POKEMON_NAMES = [
    "pikachu", "bulbasaur", "charmander", "squirtle", "eevee",
    "snorlax", "gengar", "mewtwo", "psyduck", "jigglypuff"
]

API_URL = "https://pokeapi.co/api/v2/pokemon/{}"

async def fetch_pokemon(client, name):
    url = API_URL.format(name)
    resp = await client.get(url)
    resp.raise_for_status()
    data = resp.json()
    pokemon_id = data["id"]
    types = [t["type"]["name"] for t in data["types"]]
    return {"name": name, "id": pokemon_id, "types": types}

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch_pokemon(client, name) for name in POKEMON_NAMES]
        results = await asyncio.gather(*tasks)
        for p in results:
            print(f"{p['name'].capitalize()} -> ID = {p['id']}, Types = {', '.join(p['types'])}")

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"Total time: {round(end - start, 2)} seconds")