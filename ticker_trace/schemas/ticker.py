from typing import Optional

from pydantic import BaseModel


class TickerCreate(BaseModel):
    symbol: str
    name: Optional[str] = None


class TickerUpdate(TickerCreate):
    id: int

    class Config:
        from_attributes = True
