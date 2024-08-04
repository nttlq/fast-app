from pydantic import BaseModel, ConfigDict


class CommentIn(BaseModel):
    body: str
    post_id: int


class CommentOut(CommentIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
