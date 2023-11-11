import pytest
from clients.alpha_vantage import AlphaVantage
from schemas.price import APIPrices


@pytest.mark.asyncio
@pytest.mark.default_cassette("alpha_vantage_get_prices.yaml")
@pytest.mark.vcr(record_mode="once", match_on=["uri", "method"])
async def test_get_ticker():
    api = AlphaVantage()
    response = await api.get_prices(symbol="AAPL")
    records = APIPrices(prices=response)
    assert len(records.prices) == 6047
