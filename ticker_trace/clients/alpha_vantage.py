from clients.base import AsyncHTTPClient
import settings


class AlphaVantage(AsyncHTTPClient):
    def __init__(self, api_key: str = None, function: str = None):
        super().__init__(settings.AV_API_URL)
        self.api_key = api_key or settings.AV_API_KEY
        self.function = function or "TIME_SERIES_DAILY"

    async def get_prices(
        self,
        symbol: str,
        interval: str = "60min",
        data_type: str = "json",
        output_size: str = "full",
        month: str = None,
    ):
        params = {
            "function": self.function,
            "symbol": symbol,
            "apikey": self.api_key,
            "interval": interval,
            "datatype": data_type,
            "outputsize": output_size,
            "month": month,
        }
        return await self.get("/query", params=params)
