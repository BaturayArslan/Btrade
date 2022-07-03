from kucoin_futures.client import Market
from kucoin_futures.client import Trade
from kucoin_futures.client import User
from datetime import datetime
from adapter import Adapter


class Kucoin:
    def __init__(self, session):
        self.data = session
        self.market_client = Market(url='https://api-futures.kucoin.com')
        self.trade_client = Trade(
            self.data["key"], self.data["secret"], self.data["passphrase"])
        self.user_client = User(
            self.data["key"], self.data["secret"], self.data["passphrase"])

    def get_avaible_symbols(self):
        return self.market_client.get_contracts_list()

    @Adapter.position_details_marker
    def position_details(self):
        try:

            position = self.trade_client.get_position_details(
                self.data["pair"])
            if position["currentQty"] != 0:
                return position
            else:
                return None
        except Exception as a:
            raise Exception(f"Pozisyon Detayi getirilemedi :: {str(a)}")

    @Adapter.close_position_marker
    def close_position(self):
        try:
            return self.trade_client.create_market_order(self.data["pair"], "", "", closeOrder=True)
        except Exception as a:
            print("Pozisyon Kapatilamadi:", a)


# def get_better_prices(client, symbol):
#     ticker = client.get_ticker(symbol)
#     bestBidPrice = ticker["bestBidPrice"]
#     bestAskPrice = ticker["bestAskPrice"]
#     print(
#         "{}---bestBidPrice: ".format(pd.Timestamp.now("Asia/Istanbul")), bestBidPrice)
#     print(
#         "{}---bestAskPrice: ".format(pd.Timestamp.now("Asia/Istanbul")), bestAskPrice)


# returns something like {'orderId': '6282767ff1ee30000162e981'}

    @Adapter.create_order_marker
    def create_order(self, type, amount):
        try:
            order = self.trade_client.create_market_order(
                self.data["pair"], type, self.data["leverage"], size=amount)
            return order
        except Exception as a:
            raise Exception(f"Pozisyon yaratilamadi :: {str(a)}")

    @Adapter.order_details_marker
    def get_order_detail(self, order):
        return self.trade_client.get_order_details(order)

    def current_order_list(self):
        pass

    def history_order_list(self):
        pass

    @Adapter.account_balance_marker
    def get_account_balance(self, symbol):
        try:
            overview = self.user_client.get_account_overview(symbol)
            return int(overview["accountEquity"])
        except Exception as a:
            raise Exception(f"Hesap balance alinamadi ::  {str(a)}")

    @Adapter.open_order_details_marker
    def open_order_details(self):
        return self.trade_client.get_open_order_details(self.data["pair"])

    @staticmethod
    def timestamp_to_date(timestamp):
        return datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')

    def usdt_to_lot(self, usdt: int):
        markPrice = self.market_client.get_current_mark_price(
            self.data["pair"])
        lotPrice = markPrice["value"] / 1000
        lotQnt = (usdt * self.data["leverage"]) / lotPrice
        lotQnt = int(lotQnt)

        if lotQnt == 0 or lotPrice < 0:
            raise Exception(
                "You tried to open position with too low quantity please add more dolar.")
        return lotQnt
