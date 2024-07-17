from functools import reduce
from typing import List

from core.database import Base
from models.breach import Breach
from models.data_type import DataType
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DataLeak(Base):
    __tablename__ = "data_leak"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, autoincrement=True
    )
    hash_value: Mapped[str] = mapped_column(
        String(64), primary_key=True, nullable=False
    )
    data_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_type.id"), primary_key=True, nullable=False
    )
    breach_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("breach.id"), primary_key=True, nullable=False
    )

    data_type: Mapped["DataType"] = relationship(
        "DataType", foreign_keys=[data_type_id]
    )
    breach_found: Mapped["Breach"] = relationship("Breach", foreign_keys=[breach_id])
    found_with: Mapped[List["DataType"]] = relationship(secondary="data_found_with")

    @property
    def data_type_display(self) -> str:
        if self.data_type:
            return self.data_type.display_name
        return ""

    @property
    def found_with_display(self) -> list[str]:
        if self.found_with:
            return list(map(lambda x: x.display_name, self.found_with))
        return []

    @property
    def breach_security_tips(self) -> list[str]:
        if self.breach_found and len(self.breach_found.data_breached):
            result = list(
                reduce(
                    lambda y, z: y + z,
                    map(
                        lambda x: list(map(lambda s: s.description, x.security_tips)),
                        self.breach_found.data_breached,
                    ),
                )
            )
            return result
        return []

    def __repr__(self):
        return f"DataLeak(id={self.id}, hash_value={self.hash_value}, data_type={self.data_type}, breach_found={self.breach_found}, found_with={self.found_with})"
