from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from db.database import create_db_and_tables
from routes import author, entry, auth
from auth.jwt import verify_access_token
from auth.dependencies import get_current_user
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Configuración de Jinja2
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

# Definir las rutas de la API
app.include_router(author.router, prefix="/api/authors", tags=["Authors"])
app.include_router(entry.router, prefix="/api/entries", tags=["Entries"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# Protect existing routes
@app.get("/protected-route")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}

# Manejo de excepciones globales
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred.", "error": str(exc)},
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
