from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx
import folium
load_dotenv()
app = FastAPI(title="Service Registry")

# 
# Models
#
class Services(BaseModel):
    name: str
    url: str

Services_data = {}
# 
# Routes
#

@app.get("/services")
async def get_services():
    return Services_data

@app.post("/register")
async def register_service(service: Services):
    if service.name in Services_data:
        raise HTTPException(status_code=400, detail="Service already registered")
    Services_data[service.name] = service.url
    return {"message": "Service registered successfully"}

@app.delete("/unregister/{service_name}")
async def unregister_service(service_name: str):
    if service_name not in Services_data:
        raise HTTPException(status_code=404, detail="Service not found")
    del Services_data[service_name]
    return {"message": "Service unregistered successfully"}

@app.put("/update")
async def update_service(service: Services):
    if service.name not in Services_data:
        raise HTTPException(status_code=404, detail="Service not found")
    Services_data[service.name] = service.url
    return {"message": "Service updated successfully"}

@app.get("/aggregate",response_class=HTMLResponse)
async def get_map():
    if not Services_data:
        raise HTTPException(status_code=404, detail="No services registered")
    
    map_center = [16.8151, 100.1184]
    m = folium.Map(location=map_center, zoom_start=6)
    async with httpx.AsyncClient() as client:
        for name, url in Services_data.items():
            try:
                response = await client.get(url, timeout=5.0)
                response.raise_for_status()
                data = response.json()
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
                    popup=popup_content,
                    tooltip=name
                ).add_to(m)
            except Exception as e:
                print(f"Error fetching data from {name} at {url}: {e}")
    return m._repr_html_()