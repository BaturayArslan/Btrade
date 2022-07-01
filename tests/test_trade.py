from http import HTTPStatus
import pytest
from trade import Trade
from adapter import Adapter
from wrappers.kucoin import Kucoin
from queue import Queue
import responses
import re
from typing import Type


@pytest.fixture
def set_session_like_obj():
    return dict(
        leverage=10,
        profit_trashold=30,
        loss_trashold=10,
        pair="XBTUSDM",
        exchange="kucoin",
        key="test_key",
        secret="test_secret",
        passphrase="test_passphrase",
    )


@pytest.fixture
def set_que():
    que = Queue()
    que.put({"type": "BUY", "id": 648988797, "time": 16521896210})
    return que


@pytest.fixture
def set_trade(set_session_like_obj, set_que):
    set_session_like_obj["api"] = Adapter(Kucoin(set_session_like_obj))
    return Trade(set_que, set_session_like_obj, is_testing=True)


class MockCreateOrder:
    is_called = False

    def __init__(self, *args, **kwargs):
        MockCreateOrder.is_called = True


class TestTrade:
    data = {
        "position_details_json": {
            "code": "200000",
            "data": {
                "unrealisedRoePcnt": "0.2",
                "unrealisedPnlPcnt": "0.3",
                "currentQty": 0
            }
        },
        "open_order_details_json": {
            "code": "200000",
            "data": {
                "openOrderBuySize": 0,
                "openOrderSellSize": 0
            }
        },
        "account_balance_json": {
            "code": "200000",
            "data": {
                "accountEquity": 12,
            }
        },
        "mark_price_json": {
            "code": "200000",
            "data": {
                "value": 30000,
            }
        }
    }

    @responses.activate
    def test_trade_create_order(self, set_trade: Type[Trade], monkeypatch):
        trade = set_trade
        responses.add(responses.GET, url=re.compile("https://api-futures.kucoin.com/api/v1/position"),
                      json=TestTrade.data["position_details_json"], status=HTTPStatus.OK)
        responses.add(responses.GET, url=re.compile("https://api-futures.kucoin.com/api/v1/openOrderStatistics"),
                      json=TestTrade.data["open_order_details_json"], status=HTTPStatus.OK)
        responses.add(responses.GET, url=re.compile("https://api-futures.kucoin.com/api/v1/account-overview"),
                      json=TestTrade.data["account_balance_json"], status=HTTPStatus.OK)
        responses.add(responses.GET, url=re.compile("https://api-futures.kucoin.com/api/v1/mark-price"),
                      json=TestTrade.data["mark_price_json"], status=HTTPStatus.OK)

        def mock_create_order(*args, **kwargs):
            return MockCreateOrder()

        monkeypatch.setattr(trade.api, "create_order", mock_create_order)

        trade.run()
        assert MockCreateOrder.is_called == True
