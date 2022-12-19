"""
Root function for FastAPI
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
import openapi_description
import uvicorn
from observability import (
    LOGGER,
    setting_otlp,
    PrometheusMiddleware,
    metrics
)
import settings
import clients

app = FastAPI(
    docs_url="/api",
    redoc_url=None,
    openapi_url="/api/openapi.json",
    openapi_tags=openapi_description.TAGS,
    title=openapi_description.API_DESCRIPTION["title"],
    version=openapi_description.API_DESCRIPTION["version"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setting metrics middleware
app.add_middleware(PrometheusMiddleware, app_name=settings.APP_NAME)
app.add_route("/metrics", metrics)

tracer = setting_otlp(app)
traces = tracer.get_tracer(__name__)

LOGGER = LOGGER.getChild(__name__)

#import clients

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Start middleware and return 422 error"""
    LOGGER.debug("Start Middleware")
    response = await call_next(request)
    if response.status_code == 422:
        LOGGER.warning(f"Status Code {request.status_code} on path {request}")
        response = JSONResponse(status_code=response.status_code, content={
            "code":"422.01",
            "message": "Error in the attributs"
        })
    LOGGER.debug("End middleware")
    return response

@app.exception_handler(StarletteHTTPException)
async def raise_exception(request: Request, exc: StarletteHTTPException):
    """Function to raise exception and adapt error message"""
    if exc.status_code == 404:
        LOGGER.warning(f"Status Code {exc.status_code} on path {request}")
        return JSONResponse(status_code=exc.status_code, content={
            "code":"404.01",
            "message": "Resource not found"
        })
    if exc.status_code == 500:
        LOGGER.warning(f"Status Code {exc.status_code} on path {request}")
        return JSONResponse(status_code=exc.status_code, content={
            "code":"500.01",
            "message":"Internal error"
        })
    if exc.status_code == 405:
        LOGGER.warning(f"Status Code {exc.status_code} on path {request}")
        return JSONResponse(status_code=exc.status_code, content={
            "code":"405.01",
            "message": "Method not allowed"
        })
    LOGGER.warning(f"Status Code {exc.status_code} on path {request}")
    return JSONResponse(status_code=exc.status_code, content=exc.detail)

@app.get("/")
async def root():
    """Route test"""
    return {"Hello":"World"}

app.include_router(clients.router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
