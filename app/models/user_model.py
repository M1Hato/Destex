from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.log_tokens import LogTokens
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    tokens: Mapped[list["LogTokens"]] = relationship(back_populates="user")

