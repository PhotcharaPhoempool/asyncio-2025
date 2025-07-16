import requests
import time

pokemon_names = ["pikachu", "bulbasaur", "charmander", "squirtle", "snorlax"]

start = time.time()

for name in pokemon_names:
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    data = response.json()
    print(f"Name: {data['name'].title()} -> ID: {data['id']}, Type(s): {[t["type"]["name"] for t in data["types"]]}")
   
end = time.time()
print("Total time:", round(end - start, 2),  "seconds")