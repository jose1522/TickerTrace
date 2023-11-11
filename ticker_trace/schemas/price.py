import datetime
from typing import Any, List

from pydantic import BaseModel, Field, model_validator


class APIPriceRecord(BaseModel):
    date: datetime.date
    open: float = Field(None, alias="1. open")
    high: float = Field(None, alias="2. high")
    low: float = Field(None, alias="3. low")
    close: float = Field(None, alias="4. close")
    volume: int = Field(None, alias="5. volume")


class APIPrices(BaseModel):
    records: List[APIPriceRecord]

    @model_validator(mode="before")
    def validate(cls, values: Any) -> Any:
        prices = []
        for key, value in values["records"].items():
            key = datetime.datetime.strptime(key, "%Y-%m-%d").date()
            value["date"] = key
            prices.append(value)
        values["records"] = prices
        return values


class PriceCreate(BaseModel):
    symbol: str


class PriceRecord(BaseModel):
    date: datetime.date
    open: float
    high: float
    low: float
    close: float
    volume: int
