from core.database import Base
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column


class DataFoundWith(Base):
    __tablename__ = "data_found_with"
    data_leak_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_leak.id"), primary_key=True
    )
    data_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_type.id"), primary_key=True
    )

    def __repr__(self):
        return f"FoundWith(data_leak_id={self.data_leak_id}, data_type_id={self.data_type_id})"
