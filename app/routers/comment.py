from fastapi import APIRouter, HTTPException, status

from app.routers.post import comment_table, post_table
from app.schemas import CommentIn, CommentOut

router = APIRouter(prefix="/comment", tags=["Comments"])


def find_post(post_id: int):
    return post_table.get(post_id, None)


def find_all_comments(post_id: int):
    comments = []
    for comm in comment_table.values():
        if comm.get("post_id") == post_id:
            comments.append(comm)

    return comments


@router.post("", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )

    data = comment.model_dump()
    last_comm_id = len(comment_table)
    new_comment = {**data, "id": last_comm_id}
    comment_table[last_comm_id] = new_comment

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
