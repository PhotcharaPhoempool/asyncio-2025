import time
import random
import asyncio
import httpx
from flask import Blueprint, render_template, current_app

# Create a Blueprint for async routes
async_bp = Blueprint("async", __name__)

# Helper function to fetch a single XKCD JSON by URL
async def get_xkcd(client, url):
    response = await client.get(url)
    print(f"{time.ctime()} - get {url}")    # Log the request time and URL
    return response.json()

# Helper function to fetch multiple XKCD comics
async def get_xkcds():
    # Get the number of comics to fetch from app config
    NUMBER_OF_XKCD = current_app.config.get("NUMBER_OF_XKCD", 5)

    # Generate a list of random comic numbers (0–300)
    rand_list=[random.randint(0,300) for _ in range(NUMBER_OF_XKCD)]

    xkcd_data = []
    async with httpx.AsyncClient() as client:
        tasks = []
        for number in rand_list:
            url = f'https://xkcd.com/{number}/info.0.json'
            tasks.append(get_xkcd(client, url))
        xkcd_data = await asyncio.gather(*tasks)
    return xkcd_data
    

# Route: GET /async/
@async_bp.route('/')
async def home():
    start_time = time.perf_counter()  # Start performance timer
    xkcds = await get_xkcds()               # Fetch random XKCD comics
    end_time = time.perf_counter()    # End performance timer

    # Log time and count
    print(f"{time.ctime()} - Get {len(xkcds)} xkcd. Time taken: {end_time-start_time} seconds")
    
    # Render result using Jinja2 template
    return render_template('sync.html'
                           , title="XKCD Asynchronous Flask"
                           , heading="XKCD Asynchronous Version"
                           , xkcds=xkcds
                           , end_time=end_time
                           , start_time=start_time)
