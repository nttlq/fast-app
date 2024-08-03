from pydantic import BaseModel


class CommentIn(BaseModel):
    body: str
    post_id: int


class CommentOut(CommentIn):
    id: int
