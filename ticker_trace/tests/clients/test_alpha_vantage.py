import pytest
from clients.alpha_vantage import AlphaVantage
from schemas.price import APIPrices


@pytest.mark.asyncio
@pytest.mark.default_cassette("alpha_vantage_get_prices.yaml")
@pytest.mark.vcr(record_mode="once", match_on=["uri", "method"])
async def test_get_ticker():
    api = AlphaVantage()
    response = await api.get_daily_prices(symbol="IBM")
    response = APIPrices(records=response)
    assert len(response.records) == 100
