# https://pypi.org/project/pandas/
import pdb
from shutil import ExecError
import sys
import json
from datetime import datetime
from time import sleep
from console.clparser import Parser
from adapter import Adapter
from typing import Type
from watchdog.observers import Observer
from eventhandler import event_handler


def main():
    try:
        arguments = sys.argv[1:]
        session = Parser().parse(arguments)
        api: Type[Adapter] = Adapter(session["api"])

        observer = Observer()
        observer.schedule(event_handler, "/var/www/webhook/event.txt")
        observer.start()

        event = event_handler._event

        while True:
            # Read event file for Tradingview event
            file = open("/var/www/webhook/event.txt", "r")
            content = file.read()
            file.close()
            # Keep record of previous event for compresion with new one
            prevEvent = event

            # Transform event string to json format
            event = json.loads(content)
            event["time"] = api.timestamp_to_date(event["time"])

            # Check Are we have a position or order
            position = api.position_details()
            activeOrderCount = api.open_order_details()
            if not(position) and activeOrderCount["openOrderBuySize"] == 0 and activeOrderCount["openOrderSellSize"] == 0:

                # Controls is event come ever or new event come
                if event and prevEvent["id"] != event["id"]:
                    # new event comes, Place an order with your hole budget
                    budget = int(api.account_balance("USDT"))
                    if budget > 10:
                        order = api.create_order(
                            event["type"], api.usdt_to_lot(10))
                    else:
                        order = api.create_order(
                            event["type"], api.usdt_to_lot(budget))
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
                    if unrealisedRoe > session["profit_trashold"]:
                        # close position
                        print("close, ", unrealisedRoe)
                        print(api.close_position())
                    else:
                        # remain open
                        print("remain Open, ", unrealisedRoe)
                elif unrealisedRoe < 0:
                    if unrealisedRoe < session["loss_trashold"]:
                        # close position
                        print("close, ", unrealisedRoe)
                        print(api.close_position())
                    else:
                        # remain open
                        print("remain Open, ", unrealisedRoe)
            sleep(2)
        # write function for open position
        # write function for close position
        # function for get open position information
        # design a loop
    except Exception as e:
        print(e)


main()
