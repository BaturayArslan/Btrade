# https://pypi.org/project/pandas/
from logging import exception
import pdb
from shutil import ExecError
import sys
import json
import time
import pandas as pd
from datetime import datetime
from kucoin_futures.client import Market
from kucoin_futures.client import Trade
from kucoin_futures.client import User
from time import sleep
from console.clparser import Parser
import warnings


def connection(key, secret, passphrase, user=False):
    if user:
        return User(key, secret, passphrase)
    else:
        return Trade(key, secret, passphrase)


def get_avaible_symbols(client):
    btc = client.get_contracts_list()
    btc = pd.DataFrame(btc).transpose()
    # btc.set_index('symbol', inplace=True)
    print(btc)


def position_details(client, symbol):
    try:
        position = client.get_position_details(symbol)
        if position["currentQty"] != 0:
            return position
        else:
            print("There is no position.")
    except Exception as a:
        print("Pozisyon Detayi getirilemedi: ", a)


def close_Position(client, symbol):
    try:
        return client.create_market_order(symbol, "", "", closeOrder=True)
    except Exception as a:
        print("Pozisyon Kapatilamadi:", a)


def get_better_prices(client, symbol):
    ticker = client.get_ticker(symbol)
    bestBidPrice = ticker["bestBidPrice"]
    bestAskPrice = ticker["bestAskPrice"]
    print(
        "{}---bestBidPrice: ".format(pd.Timestamp.now("Asia/Istanbul")), bestBidPrice)
    print(
        "{}---bestAskPrice: ".format(pd.Timestamp.now("Asia/Istanbul")), bestAskPrice)


# returns something like {'orderId': '6282767ff1ee30000162e981'}
def create_order(client, pair, type, lev, amount):
    try:
        order = client.create_market_order(pair, type, lev, size=amount)
        return order
    except Exception as a:
        print("Pozisyon yaratilaadi", a)


def get_order_detail(client, order):
    return client.get_order_details(order)


def current_order_list(client):
    print()


def history_order_list(client):
    print()


def get_account_balance(client, symbol):
    try:
        overview = client.get_account_overview(symbol)
        return overview["accountEquity"]
    except Exception as a:
        print("Hesap balance alinamadi, ", a)


def timestamp_to_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')


def usdt_to_lot(client, pair, lev, usdt):
    markPrice = client.get_current_mark_price(pair)
    lotPrice = markPrice["value"] / 1000
    lotQnt = (usdt * lev) / lotPrice
    return int(lotQnt)


def main():
    try:
        arguments = sys.argv[1:]
        session = Parser().parse(arguments)
        pdb.set_trace()
        api = Adapter(session["api"])

        with open("/var/www/webhook/event.txt", "r") as file:
            event = file.read()
        event = json.loads(event)

        client = Market(url='https://api-futures.kucoin.com')
        # function for create connection to account
        t_client = connection(key, secret, passPharase)
        u_client = connection(key, secret, passPharase, user=True)
        usdt_to_lot(client, pair, lev, 10)
        while True:
            # Read event file for Tradingview event
            file = open("/var/www/webhook/event.txt", "r")
            content = file.read()
            file.close()
            # Keep record of previous event for compresion with new one
            prevEvent = event

            # Transform event string to json format
            event = json.loads(content)
            event["time"] = timestamp_to_date(event["time"])

            # Check Are we have a position or order
            position = position_details(t_client, pair)
            activeOrderCount = t_client.get_open_order_details(pair)
            if not(position) and activeOrderCount["openOrderBuySize"] == 0 and activeOrderCount["openOrderSellSize"] == 0:

                # Controls is event come ever or new event come
                if event and prevEvent["id"] != event["id"]:
                    # new event comes, Place an order with your hole budget
                    budget = int(get_account_balance(u_client, "USDT"))
                    if budget > 10:
                        order = create_order(
                            t_client, pair, event["type"], lev, usdt_to_lot(client, pair, lev, 10))
                    else:
                        order = create_order(
                            t_client, pair, event["type"], lev, usdt_to_lot(client, pair, lev, budget))
                    print(event)
                    print(order)
                else:
                    # we are not in a position and thre is no new event yet
                    print("Waiting For Event.")

            else:
                # we are in a position check position status
                unrealisedPnl = float(position["unrealisedPnlPcnt"]) * 100
                unrealisedRoe = float(position["unrealisedRoePcnt"]) * 100
                if unrealisedRoe > 0:
                    if unrealisedRoe > PROFIT_TRESHHOLD:
                        # close position
                        print("close, ", unrealisedRoe)
                        print(close_Position(t_client, pair))
                    else:
                        # remain open
                        print("remain Open, ", unrealisedRoe)
                elif unrealisedRoe < 0:
                    if unrealisedRoe < STOP_TRESHHOLD:
                        # close position
                        print("close, ", unrealisedRoe)
                        print(close_Position(t_client, pair))
                    else:
                        # remain open
                        print("remain Open, ", unrealisedRoe)
            sleep(2)
        # write function for open position
        # write function for close position
        # function for get open position information
        # design a loop
    except Exception as e:
        warnings.warn("Fatal exception: {}".format(str(e)))


main()
