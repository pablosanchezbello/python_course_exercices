from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from db.database import create_db_and_tables
from routes import author, entry
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000",  # URL del frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crea la base de datos y las tablas al iniciar la aplicación
@asynccontextmanager
async def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

# Definir las rutas de la API
app.include_router(author.router, prefix="/api/authors", tags=["Authors"])
app.include_router(entry.router, prefix="/api/entries", tags=["Entries"])

# Manejo de excepciones globales
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred.", "error": str(exc)},
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
