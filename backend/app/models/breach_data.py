from core.database import Base
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column


class BreachData(Base):
    __tablename__ = "breach_data"
    breach_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("breach.id"), primary_key=True
    )
    data_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_type.id"), primary_key=True
    )

    def __repr__(self):
        return (
            f"BreachData(breach_id={self.breach_id}, data_type_id={self.data_type_id})"
        )
