from clients.base import AsyncHTTPClient
import settings


class AlphaVantage(AsyncHTTPClient):
    def __init__(self, api_key: str = None, function: str = None):
        super().__init__(settings.AV_API_URL)
        self.api_key = api_key or settings.AV_API_KEY
        self.function = function or "TIME_SERIES_DAILY"
        self.headers = {
            "Referer": "https://www.alphavantage.co/documentation/",
            "User-Agent": "Mozilla/5.0",
        }

    async def get_daily_prices(
        self,
        symbol: str,
    ):
        params = {
            "function": self.function,
            "symbol": symbol,
            "apikey": self.api_key,
        }
        response = await self.get("/query", params=params)
        return response["Time Series (Daily)"]
