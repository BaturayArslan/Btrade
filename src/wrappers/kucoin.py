from kucoin_futures.client import Market
from kucoin_futures.client import Trade
from kucoin_futures.client import User
from datetime import datetime


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

    def position_details(self):
        try:
            position = self.trade_client.get_position_details(
                self.data["pair"])
            if position["currentQty"] != 0:
                return position
            else:
                return None
        except Exception as a:
            print("Pozisyon Detayi getirilemedi: ", a)

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


    def create_order(self, type, amount):
        try:
            order = self.trade_client.create_market_order(
                self.data["pair"], type, self.data["leverage"], size=amount)
            return order
        except Exception as a:
            print("Pozisyon yaratilamadi", a)

    def get_order_detail(self, order):
        return self.trade_client.get_order_details(order)

    def current_order_list(self):
        pass

    def history_order_list(self):
        pass

    def get_account_balance(self, symbol):
        try:
            overview = self.user_client.get_account_overview(symbol)
            return overview["accountEquity"]
        except Exception as a:
            print("Hesap balance alinamadi, ", a)

    @staticmethod
    def timestamp_to_date(timestamp):
        return datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')

    def usdt_to_lot(self, usdt: int):
        markPrice = self.market_client.get_current_mark_price(
            self.data["pair"])
        lotPrice = markPrice["value"] / 1000
        lotQnt = (usdt * self.data["leverage"]) / lotPrice
        return int(lotQnt)
