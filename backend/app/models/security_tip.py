from core.database import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class SecurityTip(Base):
    __tablename__ = "security_tip"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    data_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("data_type.id"))

    def __repr__(self):
        return f"SecurityTip(id={self.id}, description={self.description} data_type_id={self.data_type_id})"
