from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str]

    def __repr__(self) -> str:
        return f"Post(id={self.id}, body={self.body})"
