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
from eventhandler import MyEventHandler
from trade import Trade
from queue import Queue


def main():
    try:
        arguments = sys.argv[1:]
        session = Parser().parse(arguments)

        que = Queue()

        event_handler = MyEventHandler(que)
        observer = Observer()
        observer.schedule(event_handler, "/var/www/webhook/event.txt")
        observer.start()

        trade = Trade(que, session)
        trade.start()

        observer.join()
        trade.join()

    except Exception as e:
        print(e)


main()
