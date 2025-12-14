import os

import pytest
import requests
import requests_mock

from market_data.client import AlpacaClient


@pytest.fixture
def client():
    os.environ["APCA_API_KEY_ID"] = "TEST_KEY"
    os.environ["APCA_API_SECRET_KEY"] = "TEST_SECRET"
    return AlpacaClient()


def test_auth_headers(client):
    """
    Test 1: Verify API keys are correctly injected into headers.
    """
    assert client.headers["APCA-API-KEY-ID"] == "TEST_KEY"
    assert client.headers["APCA-API-SECRET-KEY"] == "TEST_SECRET"


def test_pagination(client):
    """
    Test 2: Mock a multi-page response and verify the client aggregates the data
    correctly.
    """
    url = client.BASE_URL

    page1 = {
        "bars": {"AAPL": [{"t": "2023-01-01", "c": 150}]},
        "next_page_token": "token123",
    }
    page2 = {"bars": {"AAPL": [{"t": "2023-01-02", "c": 155}]}, "next_page_token": None}

    with requests_mock.Mocker() as m:
        m.get(
            url,
            [{"json": page1, "status_code": 200}, {"json": page2, "status_code": 200}],
        )

        bars = client.get_stock_bars(["AAPL"], "1Day")

        assert len(bars) == 2
        assert bars[0]["c"] == 150
        assert bars[1]["c"] == 155
        assert m.call_count == 2

        # Verify pagination token params
        history = m.request_history
        assert "page_token" not in history[0].qs
        assert history[1].qs["page_token"] == ["token123"]


def test_error_handling(client):
    """
    Test 3: Mock a 403 Forbidden response and verify the correct exception is
    raised.
    """
    with requests_mock.Mocker() as m:
        m.get(client.BASE_URL, status_code=403, reason="Forbidden")

        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            client.get_stock_bars(["AAPL"], "1Day")

        assert excinfo.value.response.status_code == 403
