import os
from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator, validator
import uvicorn
import pandas as pd
from io import BytesIO
from jinja2 import Template
from xhtml2pdf import pisa
from exceptions.location_not_found import LocationNotFoundException
from utils.api_weather import fetch_data  # Importar la función desde el archivo auxiliar
from pathlib import Path
from geopy.geocoders import Nominatim

# Initialize the geocoder
geolocator = Nominatim(user_agent="myGeocoder")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class CityModel(BaseModel):
    city: str = Field(..., min_length=1, description="Nombre de la ciudad para obtener el clima")

    @field_validator('city')
    def city_must_not_be_blank(cls, value):
        if not value.strip():
            raise ValueError('City must not be blank or contain only spaces')
        return value

# Manejo de excepciones globales
@app.exception_handler(LocationNotFoundException)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"detail": "Incorrect city.", "error": str(exc)},
    )

def extract_location_from_city(city: str = Field(..., min_length=1)):
    location = geolocator.geocode(city)
    print(location)
    if not location:
        raise LocationNotFoundException()
    print((location.latitude, location.longitude))

    return location
    
@app.get("/weather")
async def get_weather(city: str):
    try:
        city_data = CityModel(city=city)
        location = extract_location_from_city(city_data.city)
        weather_data = await fetch_data(location.latitude, location.longitude)

        return weather_data
    except Exception as e:
        return {"error": str(e)}

@app.get("/weather/excel")
async def get_weather_excel(city: str):
    try:
        city_data = CityModel(city=city)
        location = extract_location_from_city(city_data.city)
        weather_data = await fetch_data(location.latitude, location.longitude)

        # Generar el archivo Excel en memoria
        buffer = BytesIO()
        df = pd.DataFrame(weather_data)
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Weather")
        buffer.seek(0)
        # Enviar el archivo Excel al cliente
        return Response(
            buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=weather_data.xlsx"}
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/weather/csv")
async def get_weather_csv(city: str):
    try:
        city_data = CityModel(city=city)
        location = extract_location_from_city(city_data.city)
        weather_data = await fetch_data(location.latitude, location.longitude)

        # Generar el archivo CSV en memoria
        buffer = BytesIO()
        df = pd.DataFrame(weather_data)
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        # Enviar el archivo CSV al cliente
        return Response(
            buffer.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=weather_data.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/weather/pdf")
async def get_weather_pdf(request: Request, city: str):
    try:
        city_data = CityModel(city=city)
        location = extract_location_from_city(city_data.city)
        weather_data = await fetch_data(location.latitude, location.longitude)

        # Cargar la plantilla HTML desde el archivo externo
        template_path = Path("views/pdf_template.html")
        html_template = template_path.read_text(encoding="utf-8")
        template = Template(html_template)
        rendered_html = template.render(weather_data=weather_data, city=city)
        
        # Convertir el HTML a PDF con xhtml2pdf
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(rendered_html, dest=pdf_buffer)
        if pisa_status.err:
            return {"error": "Error al generar el PDF"}
        pdf_buffer.seek(0)
        
        # Enviar el archivo PDF al cliente
        return Response(
            pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=weather_data.pdf"}
        )
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
