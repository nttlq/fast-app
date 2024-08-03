from pydantic import BaseModel

from app.schemas import CommentOut


class UserPostIn(BaseModel):
    body: str


class UserPostOut(UserPostIn):
    id: int


class UserPostWithCommentsOut(BaseModel):
    post: UserPostOut
    comments: list[CommentOut]
