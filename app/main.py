import time
from contextlib import asynccontextmanager

from colorama import Fore, Style
from fastapi import FastAPI

from app.routers.comment import router as comment_router
from app.routers.post import router as post_router


class TimingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        start_time = time.time()
        await self.app(scope, receive, send)
        duration = time.time() - start_time
        print(Fore.BLUE, f"Request duration: {duration:.10f} seconds", Style.RESET_ALL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("hello")
    # TODO: Redis cache on
    yield
    print("bye")


app = FastAPI(lifespan=lifespan)

app.add_middleware(TimingMiddleware)

app.include_router(post_router)
app.include_router(comment_router)
