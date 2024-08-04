import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    res = await async_client.post("/post", json={"body": body})
    return res.json()


async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    res = await async_client.post("/comment", json={"body": body, "post_id": post_id})
    return res.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test Post11", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict):
    return await create_comment("Test Comment", created_post["id"], async_client)


# @pytest.mark.anyio
# async def test_create_post(async_client: AsyncClient):
#     body = "Test Post22"

#     res = await async_client.post("/post", json={"body": body})
#     print("res", res.status_code)
#     assert res.status_code == 201
#     assert {"id": 1, "body": body}.items() <= res.json().items()

# async def get_last_record_id():
#     async with async_session_factory() as session:
#         query = select(Comment.id).order_by(Comment.id.desc()).limit(1)
#         res = await session.execute(query)
#         await session.commit()
#         return res.scalar_one_or_none()


@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):

    res = await async_client.get("/post")
    print("res:", res)
    # assert list(post_table.values())
    assert res.status_code == 200
    assert res.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    body = "Test Comment"
    res = await async_client.post(
        "/comment", json={"body": body, "post_id": created_post["id"]}
    )

    assert res.status_code == 201
    assert {
        "id": 1,
        "body": "Test Comment",
        "post_id": created_post["id"],
    }.items() <= res.json().items()


@pytest.mark.anyio
async def test_get_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    res = await async_client.get(f"/post/{created_post['id']}/comment")
    print("res:", res.json())
    assert res.status_code == 200
    assert {
        "body": "Test Comment",
        "post_id": created_post["id"],
        "id": 2,
    }.items() <= res.json()[0].items()


@pytest.mark.anyio
async def test_create_comment_with_invalid_body(
    async_client: AsyncClient, created_post: dict
):
    body = {}
    post_id = created_post["id"]

    res = await async_client.post("/comment", json={"body": body, "post_id": post_id})

    assert res.status_code == 422


@pytest.mark.anyio
async def test_create_comment_with_invalid_postid(
    async_client: AsyncClient, created_post: dict
):
    body = "Test Comment"
    post_id = 999

    res = await async_client.post("/comment", json={"body": body, "post_id": post_id})

    assert res.status_code == 404


@pytest.mark.anyio
async def test_get_comments_on_post_empty(
    async_client: AsyncClient, created_post: dict
):
    res = await async_client.get(f"/post/{created_post['id']}/comment")

    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.anyio
async def test_create_invalid_post(async_client: AsyncClient):
    body = {}

    res = await async_client.post("/post", json=body)

    assert res.status_code == 422


@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    res = await async_client.get(f"/post/{created_post['id']}")

    assert res.status_code == 200
    assert res.json() == {"post": created_post, "comments": [created_comment]}
