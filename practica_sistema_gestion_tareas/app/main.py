import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
from routes import user, todo_list, task

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Omitir logs de SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

app = FastAPI()

# Middleware para registrar solicitudes y respuestas
@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    logger.info(f"Request: {request.method} {request.url} Body: {body.decode('utf-8') if body else 'No Body'}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

@app.get("/", response_class=JSONResponse)
def read_root(request: Request):
    return JSONResponse(
        status_code=200,
        content={"text": "Hello World!"}
    )

app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(todo_list.router, prefix="/api/lists", tags=["Lists"])
app.include_router(task.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(task.router, prefix="/api/status", tags=["Status"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)