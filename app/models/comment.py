from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Comment(id={self.id}, body={self.body}, post_id={self.post_id})"
