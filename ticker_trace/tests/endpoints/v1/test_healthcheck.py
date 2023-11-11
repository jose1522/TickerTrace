def test_healthcheck(client):
    response = client.get("/v1/healthcheck")
    assert response.status_code == 200
    assert response.json() == dict(status="ok")
