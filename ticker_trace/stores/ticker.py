from pydantic import BaseModel

from utils.exceptions import DuplicateRecordException
from .base import BaseDBTransaction
from models import Ticker


class TickerDBTransaction(BaseDBTransaction):
    def __init__(self, session):
        super().__init__(session)
        self.model = Ticker

    def add(self, obj):
        if self.get_by_symbol(obj.symbol) is None:
            super().add(obj)
        else:
            raise DuplicateRecordException(
                f"Ticker with symbol {obj.symbol} already exists"
            )

    def get_by_symbol(self, symbol):
        return self.session.query(self.model).filter_by(symbol=symbol).first()

    def get_by_name(self, name):
        return self.session.query(self.model).filter_by(name=name).first()

    def update(self, obj_id, data):
        if isinstance(data, BaseModel):
            data = data.model_dump(exclude={"id"})
        if self.get_by_symbol(data["symbol"]) is not None:
            raise DuplicateRecordException(
                f"Ticker with symbol {data['symbol']} already exists"
            )
        return super().update(obj_id, data)
