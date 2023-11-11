import freezegun
import pytest
from stores.price import PriceDBTransaction


@freezegun.freeze_time("2023-11-01")
@pytest.mark.vcr(record_mode="once", match_on=["uri", "method"])
def test_post_ticker_prices(client, session):
    symbol = "IBM"
    storage = PriceDBTransaction(session=session)
    response = client.post("/v1/ticker/", json={"symbol": symbol})
    assert response.status_code == 201
    assert len(storage.get_all()) == 100
