from clients.alpha_vantage import AlphaVantage
from schemas.price import APIPrices
from stores.price import PriceDBTransaction


async def update_price(api_key: str, symbol: str, session):
    api = AlphaVantage(api_key=api_key)
    response = await api.get_daily_prices(symbol=symbol)
    response = APIPrices(records=response).model_dump()
    with PriceDBTransaction(session=session) as storage:
        storage.bulk_insert(response["records"], symbol=symbol)
    return response
