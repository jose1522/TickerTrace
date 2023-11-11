from models import Price
from stores.base import BaseDBTransaction
from stores.ticker import TickerDBTransaction
from utils.exceptions import MissingRecordException


class PriceDBTransaction(BaseDBTransaction):
    def __init__(self, session):
        super().__init__(session=session)
        self.model = Price
        self.ticker_store = TickerDBTransaction(session=session)

    def get_by_symbol(self, symbol, page=None, page_size=None):
        ticker = self.ticker_store.get_by_symbol(symbol=symbol)
        if not ticker:
            raise MissingRecordException(f"Ticker with symbol {symbol} does not exist")
        return self.query(ticker_id=ticker.id, page=page, page_size=page_size)

    def bulk_insert(self, data, symbol: str = None):
        ticker = self.ticker_store.get_by_symbol(symbol)
        for record in data:
            record["ticker_id"] = ticker.id
        super().bulk_insert(data=data)
