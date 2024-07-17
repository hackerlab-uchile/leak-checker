from core.database import Base
from models.data_type import DataType
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    data_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_type.id"), nullable=False
    )
    data_type: Mapped["DataType"] = relationship(
        "DataType", foreign_keys=[data_type_id]
    )

    def __repr__(self):
        return f"User(id={self.id}, data={self.value} data_type_id={self.data_type_id})"
