from typing import Optional, List

from sqlalchemy.orm import Mapped, MappedColumn, relationship

from models.base import BaseModel


class Ticker(BaseModel):
    __tablename__ = "ticker"

    symbol: Mapped[str] = MappedColumn(unique=True)
    name: Mapped[Optional[str]]
    prices: Mapped[List["Price"]] = relationship(
        back_populates="ticker", cascade="all, delete-orphan"
    )
