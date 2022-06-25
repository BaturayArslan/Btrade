from re import A
from threading import Thread
from typing import Type
from queue import Queue

from numpy import negative
from session import Session
from adapter import Adapter
from time import sleep


class Trade(Thread):

    def __init__(self, que: Type[Queue], session: Type[Session]):
        self.que = que
        self.api: Type[Adapter] = session["api"]
        self.session = session

        Thread.__init__(self)
        self.setName("Trade")

    def run(self) -> None:
        while True:

            # Check Are we have a position or order
            position = self.api.position_details()
            activeOrderCount = self.api.open_order_details()
            if not(position) and activeOrderCount["openOrderBuySize"] == 0 and activeOrderCount["openOrderSellSize"] == 0:

                event = self.que.get()
                # new event comes, Place an order with your hole budget
                budget = int(self.api.account_balance("USDT"))
                if budget > 10:
                    order = self.api.create_order(
                        event["type"], self.api.usdt_to_lot(10))
                else:
                    order = self.api.create_order(
                        event["type"], self.api.usdt_to_lot(budget))
                print(order)
                print(event)
            else:
                # we are in a position check position status
                unrealisedPnl = float(position["unrealisedPnlPcnt"]) * 100
                unrealisedRoe = float(position["unrealisedRoePcnt"]) * 100
                if unrealisedRoe > 0:
                    if unrealisedRoe > self.session["profit_trashold"]:
                        # close position
                        print("close, ", unrealisedRoe)
                        print(self.api.close_position())
                    else:
                        # remain open
                        print("remain Open, ", unrealisedRoe)
                elif unrealisedRoe < 0:
                    if unrealisedRoe < -abs(self.session["loss_trashold"]):
                        # close position
                        print("close, ", unrealisedRoe)
                        print(self.api.close_position())
                    else:
                        # remain open
                        print("remain Open, ", unrealisedRoe)
                sleep(1)
