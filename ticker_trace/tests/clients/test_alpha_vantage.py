import pytest
from clients.alpha_vantage import AlphaVantage


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_ticker():
    api = AlphaVantage()
    response = await api.get_prices(symbol="AAPL")
    assert response["Meta Data"]["2. Symbol"] == "AAPL"
