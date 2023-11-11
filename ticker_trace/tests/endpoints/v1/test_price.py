import freezegun
import pytest
from stores.price import PriceDBTransaction


@freezegun.freeze_time("2023-11-01")
@pytest.mark.default_cassette("alpha_vantage_get_prices.yaml")
@pytest.mark.vcr(record_mode="once", match_on=["uri", "method"])
def test_post_ticker_prices(client, session):
    symbol = "AAPL"
    storage = PriceDBTransaction(session=session)
    response = client.post("/v1/ticker/", json={"symbol": symbol})
    assert response.status_code == 201
    response = client.post("/v1/price/", json={"symbol": symbol})
    assert response.status_code == 201
    assert len(storage.get_all()) == 6047
