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
    try:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        return {
            "name": data["name"].capitalize(),
            "id": data["id"],
            "base_experience": data["base_experience"]
        }
    except Exception as e:
        print(f"Error fetching {name}: {e}")
        return None

def sort_by_base_experience(pokemon):
    return pokemon["base_experience"]

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch_pokemon(client, name) for name in names]
        results = await asyncio.gather(*tasks)
        clean_results = [res for res in results if res is not None]
        sorted_pokemon = sorted(clean_results, key=sort_by_base_experience, reverse=True)

    for p in sorted_pokemon:
        print(f"{p["name"]:<12}\t --> ID:{p["id"]:<5} Base XP:{p["base_experience"]:<16}")

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"Total time: {round(end - start, 2)} seconds")