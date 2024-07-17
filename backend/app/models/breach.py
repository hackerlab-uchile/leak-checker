from functools import reduce
from typing import List

from core.database import Base
from models.data_type import DataType
from sqlalchemy import Boolean, Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Breach(Base):
    __tablename__ = "breach"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(1000))
    breach_date: Mapped[Date] = mapped_column(Date)
    confirmed: Mapped[bool] = mapped_column(Boolean)
    is_sensitive: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    data_breached: Mapped[List["DataType"]] = relationship(secondary="breach_data")

    @property
    def data_types(self) -> list[str]:
        if self.data_breached:
            return list(map(lambda x: x.name, self.data_breached))
        return []

    @property
    def display_data_types(self) -> list[str]:
        if self.data_breached:
            return list(map(lambda x: x.display_name, self.data_breached))
        return []

    @property
    def security_tips(self) -> list[str]:
        if len(self.data_breached):
            result = list(
                reduce(
                    lambda y, z: y + z,
                    map(
                        lambda x: list(map(lambda s: s.description, x.security_tips)),
                        self.data_breached,
                    ),
                )
            )
            return result
        return []

    # def __repr__(self):
    #     return f"Breach(id={self.id}, name={self.name}, description={self.description[:10]}[...], breach_date={self.breach_date}), data_breached={self.data_breached}"
    def __repr__(self):
        return "Breach(id={}, name={}, description={}, breach_date={}, confirmed={}, is_sensitive={}, created_at={}, data_breached={})".format(
            self.id,
            self.name,
            self.description,
            self.breach_date,
            self.confirmed,
            self.is_sensitive,
            self.created_at,
            self.data_breached,
        )
