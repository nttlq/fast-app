import logging
import time
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from app.logging_conf import configure_logging
from app.routers.comment import router as comment_router
from app.routers.post import router as post_router


class TimingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        start_time = time.time()
        await self.app(scope, receive, send)
        duration = time.time() - start_time
        logger.debug(f"Request duration: {duration:.10f} seconds")


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    configure_logging()
    # TODO: Redis cache on
    yield
    print("bye")


app = FastAPI(lifespan=lifespan)

app.add_middleware(TimingMiddleware)
app.add_middleware(CorrelationIdMiddleware, header_name="X-Correlation-ID")
app.include_router(post_router)
app.include_router(comment_router)


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
