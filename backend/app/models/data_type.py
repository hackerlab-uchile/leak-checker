from typing import List

from core.database import Base
from models.security_tip import SecurityTip
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DataType(Base):
    __tablename__ = "data_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    display_name: Mapped[str] = mapped_column(String(100))

    security_tips: Mapped[List["SecurityTip"]] = relationship()

    @property
    def display_security_tips(self) -> list[str]:
        if len(self.security_tips):
            return list(map(lambda x: x.description, self.security_tips))
        return []

    def __repr__(self):
        return f"DataType(id={self.id}, name={self.name})"
