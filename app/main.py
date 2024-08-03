from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers.comment import router as comment_router
from app.routers.post import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("hello")
    # TODO: Redis cache on
    yield
    print("bye")


app = FastAPI(lifespan=lifespan)

app.include_router(post_router)
app.include_router(comment_router)
