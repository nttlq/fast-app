from fastapi import APIRouter, HTTPException, status
from sqlalchemy import and_, select

from app.database import async_session_factory
from app.models import Comment, Post
from app.routers.post import comment_table
from app.schemas import CommentIn, CommentOut

router = APIRouter(prefix="/comment", tags=["Comments"])


async def find_post(post_id: int):
    async with async_session_factory() as session:
        query = select(Post).where(Post.id == post_id)
        res = await session.execute(query)
        await session.commit()
        return res.scalar_one_or_none()


def find_all_comments(post_id: int):
    comments = []
    for comm in comment_table.values():
        if comm.get("post_id") == post_id:
            comments.append(comm)

    return comments


async def get_last_record_id():
    async with async_session_factory() as session:
        query = select(Comment.id).order_by(Comment.id.desc()).limit(1)
        res = await session.execute(query)
        await session.commit()
        return res.scalar_one_or_none()


@router.post("", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentIn):
    post = await find_post(comment.post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )

    data = comment.model_dump()
    last_comm_id = await get_last_record_id()
    new_comment = {**data, "id": last_comm_id + 1 if last_comm_id is not None else 1}
    # comment_table[last_comm_id] = new_comment

    async with async_session_factory() as session:
        stmt = Comment(body=comment.body, post_id=comment.post_id)
        session.add(stmt)
        await session.commit()

    return new_comment


@router.get("", response_model=list[CommentOut])
async def get_all_comments(post_id: int):
    post = find_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )
    print(f"all comments: {comment_table}")
    comments = find_all_comments(post_id)
    if comments == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comments not found"
        )

    return comments
