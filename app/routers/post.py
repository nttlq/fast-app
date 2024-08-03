from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from sqlalchemy import and_, select

from app.database import async_session_factory
from app.models import Comment, Post
from app.schemas import CommentOut, UserPostIn, UserPostOut, UserPostWithCommentsOut

router = APIRouter(prefix="/post", tags=["Posts"])


post_table = {}
comment_table = {}


async def find_post(post_id: int):
    async with async_session_factory() as session:
        query = select(Post).where(Post.id == post_id)
        res = await session.execute(query)
        await session.commit()

        return res.scalars().all()


async def get_last_record_id():
    async with async_session_factory() as session:
        query = select(Post.id).order_by(Post.id.desc()).limit(1)
        res = await session.execute(query)
        await session.commit()
        return res.scalar_one()


@router.get("", response_model=list[UserPostOut])
async def get_all_posts():
    """Get all posts from the database"""
    async with async_session_factory() as session:
        query = select(Post)
        result = await session.execute(query)
        await session.commit()
        return result.scalars().all()


@router.post("", response_model=UserPostOut, status_code=status.HTTP_201_CREATED)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_record_id = await get_last_record_id()
    new_post = {**data, "id": last_record_id + 1}
    print(f"{data}")
    print(new_post)
    async with async_session_factory() as session:
        stmt = Post(body=post.body)
        session.add(stmt)
        await session.commit()
        return new_post


@router.get("/{post_id}/comment", response_model=list[CommentOut])
async def get_comments_on_post(post_id: Annotated[int, Path(ge=0)]):
    async with async_session_factory() as session:
        query = select(Comment).where(Comment.post_id == post_id)
        res = await session.execute(query)
        await session.commit()
        return res.scalars().all()


@router.get("/{post_id}", response_model=UserPostWithCommentsOut)
async def get_post_with_comments(post_id: Annotated[int, Path(ge=0)]):
    post = await find_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return {
        "post": post[0],
        "comments": await get_comments_on_post(post_id),
    }


@router.get("/check")
async def check_db():
    async with async_session_factory() as session:
        query = select(Post.body).where(and_(Post.body == "New post", Post.id == 1))
        result = await session.execute(query)
        await session.commit()
        return result.scalars().all()
