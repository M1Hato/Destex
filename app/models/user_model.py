from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.log_tokens import LogTokens
from app.models.task_model import Task
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    tokens: Mapped[list["LogTokens"]] = relationship(back_populates="user")
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")

