"""
Observability definition
Code from https://github.com/Blueswen/fastapi-observability
"""
import logging
import logging.config
import time
from typing import Tuple
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from starlette.types import ASGIApp
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint
)
from prometheus_client import (
    REGISTRY,
    Counter,
    Gauge,
    Histogram
)
from prometheus_client.openmetrics.exposition import (
    CONTENT_TYPE_LATEST,
    generate_latest
)
import settings

INFO = Gauge(
    "fastapi_app_info", "FastAPI application information.", [
        "app_name"]
)
REQUESTS = Counter(
    "fastapi_requests_total", "Total count of requests by method and path.", [
        "method", "path", "app_name"]
)
RESPONSES = Counter(
    "fastapi_responses_total",
    "Total count of responses by method, path and status codes.",
    ["method", "path", "status_code", "app_name"],
)
REQUESTS_PROCESSING_TIME = Histogram(
    "fastapi_requests_duration_seconds",
    "Histogram of requests processing time by path (in seconds)",
    ["method", "path", "app_name"],
)
EXCEPTIONS = Counter(
    "fastapi_exceptions_total",
    "Total count of exceptions raised by path and exception type",
    ["method", "path", "exception_type", "app_name"],
)
REQUESTS_IN_PROGRESS = Gauge(
    "fastapi_requests_in_progress",
    "Gauge of requests by method and path currently being processed",
    ["method", "path", "app_name"],
)

logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger(settings.APP_NAME)

tracer = TracerProvider()

class PrometheusMiddleware(BaseHTTPMiddleware):
    """Add function to HTTP Middleware"""
    def __init__(self, app: ASGIApp, app_name: str = "fastapi-app") -> None:
        """Init middleware"""
        super().__init__(app)
        self.app_name = app_name
        INFO.labels(app_name=self.app_name).inc()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Add Metrics informations"""
        method = request.method
        path, is_handled_path = self.get_path(request)
        response_status_code = 0

        if not is_handled_path:
            return await call_next(request)

        REQUESTS_IN_PROGRESS.labels(
            method=method, path=path, app_name=self.app_name).inc()
        REQUESTS.labels(method=method, path=path, app_name=self.app_name).inc()
        before_time = time.perf_counter()
        try:
            response = await call_next(request)
        except BaseException as e:
            response_status_code = HTTP_500_INTERNAL_SERVER_ERROR
            EXCEPTIONS.labels(method=method, path=path, exception_type=type(
                e).__name__, app_name=self.app_name).inc()
            raise e from None
        else:
            response_status_code = response.status_code
            after_time = time.perf_counter()
            # retrieve trace id for exemplar
            span = trace.get_current_span()
            trace_id = trace.format_trace_id(
                span.get_span_context().trace_id)

            REQUESTS_PROCESSING_TIME.labels(method=method, path=path, app_name=self.app_name)\
                .observe(
                    after_time - before_time, exemplar={'TraceID': trace_id}
                )
        finally:
            RESPONSES.labels(method=method, path=path,
                             status_code=response_status_code, app_name=self.app_name).inc()
            REQUESTS_IN_PROGRESS.labels(
                method=method, path=path, app_name=self.app_name).dec()

        return response

    @staticmethod
    def get_path(request: Request) -> Tuple[str, bool]:
        """Function to check request.path and authorize"""
        for route in request.app.routes:
            match, _ = route.matches(request.scope)
            if match == Match.FULL:
                return route.path, True
        return request.url.path, False


def metrics(request: Request) -> Response:
    """Metrics configuration"""
    return Response(generate_latest(REGISTRY), headers={"Content-Type": CONTENT_TYPE_LATEST})

def setting_otlp(app: ASGIApp) -> TracerProvider():
    """Traces configuration"""
    resource = Resource(attributes={
        "service.name": settings.APP_NAME,
        "job": "Backend",
        "host": "FastAPI",
        "agent": "OTel"
    })

    # Set the trace provider
    global tracer
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)

    otlp_exporter = OTLPSpanExporter(endpoint=f"{settings.OTEL_PROTOCOL}://{settings.OTEL_HOST}:\
        {settings.OTEL_PORT}{settings.OTEL_PATH}")

    tracer.add_span_processor(BatchSpanProcessor(otlp_exporter))

    LoggingInstrumentor().instrument(set_logging_format=True)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)

    return tracer

# Start HTTP server to expose Prometheus metrics
# prom_server = start_http_server(settings.PROMETHEUS_PORT)
