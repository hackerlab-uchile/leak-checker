from core.database import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Password(Base):
    __tablename__ = "password"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hash_password: Mapped[str] = mapped_column(String(64), unique=True)
    count: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"Password(id={self.id}, hash_password={self.hash_password}, count={self.count})"
