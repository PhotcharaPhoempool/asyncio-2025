from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
import os
import folium

load_dotenv()
app = FastAPI(title="Student Service")

# 
# Models
#
class Services(BaseModel):
    name: str
    url: str

# 
# Routes
#

@app.get("/weather")
async def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={os.getenv("LAT")}&lon={os.getenv("LON")}&appid={os.getenv("OWM_API_KEY")}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch weather data")
        data = response.json()
    
    return {
        "Province": os.getenv("CITY"),
        "Temperature": data["main"]["temp"],
        "Humidity": data["main"]["humidity"],
        "Weather": data["weather"][0]["description"],
    }
    
@app.post("/register_self") #Register to service registry
async def register_service():
    service_data = {
        "name": os.getenv("STUDENT_NAME"),
        "url": os.getenv("SELF_URL")
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{os.getenv('SERVICE_REGISTRY_URL')}/register", json=service_data)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to register service")
        return {"message": "Service registered successfully"}
    
@app.delete("/unregister_self") #Unregister from service registry
async def unregister_service():
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{os.getenv('SERVICE_REGISTRY_URL')}/unregister/{os.getenv('STUDENT_NAME')}")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to unregister service")
        return {"message": "Service unregistered successfully"}
    
@app.put("/update_self")
async def update_service():
    service_data = {
        "name": os.getenv("STUDENT_NAME"),
        "url": os.getenv("SELF_URL")
    }
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{os.getenv('SERVICE_REGISTRY_URL')}/update", json=service_data)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to update service")
        return {"message": "Service updated successfully"}
    
@app.get("/aggregate", response_class=HTMLResponse)
async def get_map():
    map_center = [os.getenv("LAT"), os.getenv("LON")]
    m = folium.Map(location=map_center, zoom_start=6)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{os.getenv('SERVICE_REGISTRY_URL')}/services", timeout=5.0)
            response.raise_for_status()
            services = response.json()
            for name, url in services.items():
                try:
                    resp = await client.get(url, timeout=5.0)
                    resp.raise_for_status()
                    data = resp.json()
                    lat = data.get("lat", map_center[0])
                    lon = data.get("lon", map_center[1])
                    popup_content = f"""
                    <b>Service:</b> {name}<br>
                    <b>Province:</b> {data.get('Province', 'N/A')}<br>
                    <b>Temperature:</b> {data.get('Temperature', 'N/A')} Â°C<br>
                    <b>Humidity:</b> {data.get('Humidity', 'N/A')}%<br>
                    <b>Weather:</b> {data.get('Weather', 'N/A')}
                    """
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_content, max_width=300),
                        tooltip=name
                    ).add_to(m)
                except Exception as e:
                    print(f"Error fetching data from {name} at {url}: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to fetch services") from e
    
    return m._repr_html_()