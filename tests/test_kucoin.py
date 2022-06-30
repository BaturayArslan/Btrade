from http import HTTPStatus
import pytest
import responses
from wrappers.kucoin import Kucoin
from kucoin_futures.base_request.base_request import KucoinFuturesBaseRestApi
from typing import Type
import re


@pytest.fixture
def set_session_like_dict():
    return dict(
        leverage=10,
        profit_trashold=30,
        loss_trashold=10,
        pair="XBTUSDM",
        exchange="kucoin",
        key="test_key",
        secret="test_secret",
        passphrase="test_passphrase",
        api=None
    )


@pytest.fixture
def set_clients(set_session_like_dict) -> Type[Kucoin]:
    session = set_session_like_dict

    return Kucoin(session)


class TestKucoin:
    @pytest.mark.parametrize(
        "data,status_code,expected",
        [
            (
                {
                    "code": "200000",
                    "data": {
                        "accountEquity": 10
                    }
                },
                HTTPStatus.OK,
                10
            ),
            (
                {
                    "code": "200000",
                    "data": {
                        "accountEquity": "10"
                    }
                },
                HTTPStatus.OK,
                10
            ),
            (
                {
                    "code": "200000",
                    "data": None
                },
                HTTPStatus.NOT_FOUND,
                Exception

            )
        ]
    )
    @responses.activate
    def test_get_account_balance(self, set_clients: Type[Kucoin], data, status_code, expected):
        client = set_clients

        responses.add(responses.GET, url=re.compile("https://api-futures.kucoin.com/.*"),
                      json=data, status=status_code)
        try:
            result = client.get_account_balance("XBTUSDM")
            assert expected == result
        except Exception as a:
            assert "Hesap balance alinamadi :: " in a.args[0]

    @pytest.mark.parametrize(
        "data",
        [
            (
                {
                    "code": "200000",
                    "data": {
                        "value": 30000
                    }
                }

            )
        ]
    )
    @responses.activate
    def test_usdt_to_lot(self, set_clients: Type[Kucoin], data):
        client = set_clients

        responses.add(responses.GET, url=re.compile("https://api-futures.kucoin.com/.*"),
                      json=data, status=HTTPStatus.OK)
        assert 3 == client.usdt_to_lot(10)

        with pytest.raises(Exception) as e:
            client.usdt_to_lot(2)
        assert "You tried to open" in str(e.value)
