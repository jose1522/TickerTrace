from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn
from typing import Optional
from datetime import datetime


class BaseModel(DeclarativeBase):
    __abstract__ = True
    id: Mapped[Optional[int]] = MappedColumn(primary_key=True, autoincrement=True)
    created_at: Mapped[Optional[datetime]] = MappedColumn(default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = MappedColumn(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"

    def __str__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"
