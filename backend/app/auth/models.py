from sqlalchemy.orm import Mapped, mapped_column
from app.dao.database import Base, str_uniq
from sqlalchemy import Boolean, Date, Integer, String, text


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[Date] = mapped_column(Date, server_default=text("CURRENT_DATE"))

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
