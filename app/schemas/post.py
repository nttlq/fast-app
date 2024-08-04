from pydantic import BaseModel, ConfigDict

from app.schemas import CommentOut


class UserPostIn(BaseModel):
    body: str


class UserPostOut(UserPostIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserPostWithCommentsOut(BaseModel):
    post: UserPostOut
    comments: list[CommentOut]
