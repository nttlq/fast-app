from fastapi import APIRouter, HTTPException

from app.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

router = APIRouter()


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


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    print(f"{data}")
    post_table[last_record_id] = new_post
    return new_post


@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not Found")

    data = comment.model_dump()
    last_comm_id = len(comment_table)
    new_comment = {**data, "id": last_comm_id}
    comment_table[last_comm_id] = new_comment

    return new_comment


@router.get("/comment", response_model=list[Comment])
async def get_all_comments(post_id: int):
    post = find_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not Found")
    print(f"all comments: {comment_table}")
    comments = find_all_comments(post_id)
    if comments == []:
        raise HTTPException(status_code=404, detail="Comments not found")

    return comments


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    return [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
