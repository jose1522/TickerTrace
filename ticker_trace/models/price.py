import datetime

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import Mapped, MappedColumn, relationship

from models.base import BaseModel


class Price(BaseModel):
    __tablename__ = "price"

    date: Mapped[datetime.date] = MappedColumn(nullable=False)
    open: Mapped[float]
    close: Mapped[float]
    high: Mapped[float]
    low: Mapped[float]
    volume: Mapped[int]
    ticker_id: Mapped[int] = Column(
        ForeignKey("ticker.id", ondelete="CASCADE"), nullable=False
    )
    ticker: Mapped["Ticker"] = relationship(back_populates="prices")
