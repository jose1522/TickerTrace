import pytest

from stores.ticker import TickerDBTransaction


def test_add_new_ticker(client, session):
    ticker = TickerDBTransaction(session)
    assert ticker.get(1) is None
    response = client.post(
        "/v1/ticker/",
        json={"symbol": "IBM", "name": "IBM Inc."},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201
    assert ticker.get(1).symbol == "IBM"


def test_add_new_ticker_with_duplicate_symbol(client, session):
    ticker = TickerDBTransaction(session)
    assert ticker.get(1) is None
    response = client.post(
        "/v1/ticker/",
        json={"symbol": "IBM", "name": "IBM Inc."},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201
    response = client.post(
        "/v1/ticker/",
        json={"symbol": "IBM", "name": "IBM Inc."},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Ticker with symbol IBM already exists"}


def test_get_ticket_by_id(client, session):
    data = {"symbol": "IBM", "name": "IBM Inc."}
    with TickerDBTransaction(session) as ticker:
        assert ticker.get(1) is None
        ticker.add(ticker.new_object(data))
    response = client.get("/v1/ticker/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "symbol": "IBM", "name": "IBM Inc."}


@pytest.mark.parametrize(
    ("symbol", "name"),
    (("AAPL", "Apple Inc."), ("TSLA", "Tesla Inc.")),
    ids=("AAPL", "TSLA"),
)
def test_get_ticket_by_query_param(client, session, symbol, name):
    data = {"symbol": symbol, "name": name}
    response = client.get(f"/v1/ticker/?symbol={symbol}")
    assert response.json() == []
    with TickerDBTransaction(session) as ticker:
        ticker.add(ticker.new_object(data))
    response = client.get(f"/v1/ticker/?symbol={symbol}")
    assert response.json() == [{"id": 1, "symbol": symbol, "name": name}]
    response = client.get(f"/v1/ticker/?name={name}")
    assert response.json() == [{"id": 1, "symbol": symbol, "name": name}]
    response = client.get(f"/v1/ticker/?symbol={symbol}&name={name}")
    assert response.json() == [{"id": 1, "symbol": symbol, "name": name}]


def test_get_all_tickers(client, session):
    data = [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "TSLA", "name": "Tesla Inc."},
    ]
    ticker = TickerDBTransaction(session)
    for item in data:
        ticker.add(ticker.new_object(item))
        ticker.session.commit()
    response = client.get("/v1/ticker/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_ticker(client, session):
    ticker = TickerDBTransaction(session)
    assert ticker.get(1) is None
    ticker.add(ticker.new_object({"symbol": "AAPL", "name": "Apple Inc."}))
    ticker.session.commit()
    response = client.put("/v1/ticker/1", json={"symbol": "TSLA", "name": "Tesla"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "symbol": "TSLA", "name": "Tesla"}
    assert ticker.get(1).symbol == "TSLA"


def test_update_missing_record(client, session):
    ticker = TickerDBTransaction(session)
    assert ticker.get(1) is None
    response = client.put("/v1/ticker/1", json={"symbol": "TSLA", "name": "Tesla"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticker with id 1 does not exist"}
