"""
Root function for FastAPI
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
import openapi_description
import uvicorn
import logging
from observability import LOGGER, setting_otlp, PrometheusMiddleware, metrics, EndpointFilter
import settings

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
LOGGER.addFilter(EndpointFilter())
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
# LOGGER = logging.getLogger(settings.APP_NAME)

import clients

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    LOGGER.debug("Start Middleware")
    response = await call_next(request)
    if response.status_code == 422:
        LOGGER.warn("Status Code %s on path %s" % (response.status_code, request.path))
        response = JSONResponse(status_code=response.status_code, content={
            "code":"422.01",
            "message": "Error in the attributs"
        })
    LOGGER.debug("End middleware")
    return response

@app.exception_handler(StarletteHTTPException)
async def raise_exception(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        LOGGER.warn("Status Code %s on path %s" % (exc.status_code, request.path))
        return JSONResponse(status_code=exc.status_code, content={
            "code":"404.01",
            "message": "Resource not found"
        })
    elif exc.status_code == 500:
        LOGGER.warn("Status Code %s on path %s" % (exc.status_code, request.path))
        return JSONResponse(status_code=exc.status_code, content={
            "code":"500.01",
            "message":"Internal error"
        })
    elif exc.status_code == 405:
        LOGGER.warn("Status Code %s on path %s" % (exc.status_code, request.path))
        return JSONResponse(status_code=exc.status_code, content={
            "code":"405.01",
            "message": "Method not allowed"
        })
    else:
        LOGGER.warn("Status Code %s on path %s" % (exc.status_code, request.path))
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

@app.get("/")
async def root():
    return {"Hello":"World"}

app.include_router(clients.router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
