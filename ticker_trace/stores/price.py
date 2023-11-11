from models import Price, Ticker
from stores.base import BaseDBTransaction
from stores.ticker import TickerDBTransaction
from utils.exceptions import MissingRecordException


class PriceDBTransaction(BaseDBTransaction):
    def __init__(self, session):
        super().__init__(session=session)
        self.model = Price
        self.ticker_store = TickerDBTransaction(session=session)

    def get_by_symbol(
        self, symbol, page=None, page_size=None, start_date=None, end_date=None
    ):
        ticker = self.ticker_store.get_by_symbol(symbol=symbol)
        if not ticker:
            raise MissingRecordException(f"Ticker with symbol {symbol} does not exist")
        query = self.session.query(self.model).filter(Ticker.id == ticker.id)
        if start_date:
            query = query.filter(self.model.date >= start_date)
        if end_date:
            query = query.filter(self.model.date <= end_date)
        if page and page_size:
            skip = (page - 1) * page_size
            query = query.limit(page_size).offset(skip)
        return query.all()

    def bulk_insert(self, data, symbol: str = None):
        ticker = self.ticker_store.get_by_symbol(symbol)
        for record in data:
            record["ticker_id"] = ticker.id
        super().bulk_insert(data=data)
