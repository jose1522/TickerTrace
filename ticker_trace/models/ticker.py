from typing import Optional

from sqlalchemy.orm import Mapped, MappedColumn

from .base import BaseModel


class Ticker(BaseModel):
    __tablename__ = "ticker"
    symbol: Mapped[str] = MappedColumn(unique=True)
    name: Mapped[Optional[str]]
