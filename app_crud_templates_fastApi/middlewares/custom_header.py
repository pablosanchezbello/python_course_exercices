from fastapi import Request
from starlette.responses import Response

async def add_custom_header(request: Request, call_next):
    print("middleware 2: custom_header")
    response: Response = await call_next(request)
    response.headers["X-Custom-Header"] = "FastAPI-Demo"
    return response
