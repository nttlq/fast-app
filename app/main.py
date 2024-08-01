from enum import Enum, StrEnum
from typing import Annotated

import starlette.status
from fastapi import FastAPI, Query

from app.routers.post import router as post_router

app = FastAPI()

app.include_router(post_router)

country_dict = {
    "Russia": ["Moscow", "St. Petersburg", "Novosibirsk", "Ekaterinburg", "Kazan"],
    "USA": ["New York", "Los Angeles", "Chicago", "Houston", "Philadelphia"],
}


class Country(str, Enum):
    russia = "Russia"
    usa = "USA"


@app.get("/product/{id}")
async def detail_view(id: int):
    return {"product": f"Stock number {id}"}


@app.get("/users")
async def users(name: Annotated[str | None, Query()] = None, age: int = 30):
    return {"user_name": name, "user_age": age}


@app.get("/users/{name}/{age}")
async def users_old(name: str, age: int):
    return {"user_name": name, "user_age": age}


from fastapi import Cookie, HTTPException
from starlette import status


@app.get("/country/{country}")
async def list_cities(country: Country, limit: int | None = None):
    values = country_dict.get(country.value)
    if not values:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "Not Found"}
        )

    return {"country": country, "cities": list(values)[:limit]}
