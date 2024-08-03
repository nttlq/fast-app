from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from app.schemas import CommentOut, UserPostIn, UserPostOut, UserPostWithCommentsOut

router = APIRouter(prefix="/post", tags=["Posts"])


post_table = {}
comment_table = {}


def find_post(post_id: int):
    return post_table.get(post_id, None)


def find_all_comments(post_id: int):
    comments = []
    for comm in comment_table.values():
        if comm.get("post_id") == post_id:
            comments.append(comm)

    return comments


@router.get("", response_model=list[UserPostOut])
async def get_all_posts():
    return list(post_table.values())


@router.post("", response_model=UserPostOut, status_code=status.HTTP_201_CREATED)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    print(f"{data}")
    post_table[last_record_id] = new_post
    return new_post


@router.get("/{post_id}/comment", response_model=list[CommentOut])
async def get_comments_on_post(post_id: Annotated[int, Path(ge=0)]):
    return [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]


@router.get("/{post_id}", response_model=UserPostWithCommentsOut)
async def get_post_with_comments(post_id: Annotated[int, Path(ge=0)]):
    post = find_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }


from sqlalchemy import and_, or_, select

from app.database import async_session_factory
from app.models import Post


@router.get("/check")
async def check_db():
    async with async_session_factory() as session:
        query = select(Post.body).where(and_(Post.body == "New post", Post.id == 1))
        result = await session.execute(query)
        await session.commit()
        return result.scalars().all()
