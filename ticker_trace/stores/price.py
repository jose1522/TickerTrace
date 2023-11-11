from models import Price
from stores.base import BaseDBTransaction


class PriceDBTransaction(BaseDBTransaction):
    def __init__(self, session):
        super().__init__(session=session)
        self.model = Price

    def get_by_ticker(self, ticker_id, page=None, page_size=None):
        return self.query(ticker_id=ticker_id, page=page, page_size=page_size)
