from core.config import CODE_LENGTH
from core.database import Base
from models.user import User
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class VerificationCode(Base):
    __tablename__ = "verification_code"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(length=CODE_LENGTH), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    address: Mapped[str] = mapped_column(String, nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=false(), nullable=False)
    tries: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    user_owner: Mapped["User"] = relationship("User", foreign_keys=[user_id])

    @property
    def associated_value(self) -> str:
        if self.user_owner:
            return self.user_owner.value
        return ""

    @property
    def value_type(self) -> str:
        if self.user_owner:
            return self.user_owner.data_type.name
        return ""

    @property
    def format_code_to_send(self) -> str:
        if self.code:
            half_length = len(self.code) // 2
            return f"{self.code[:half_length]}-{self.code[half_length:]}"
        return ""

    def __repr__(self):
        return f"VerificationCode(id={self.id}, code={self.code}, created_at={self.created_at}, user_owner={self.user_owner}, used={self.used}, tries={self.tries})"
