import sys
from console.clparser import Parser
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
        observer.daemon = True
        observer.start()

        trade = Trade(que, session)
        trade.daemon = True
        trade.start()

        observer.join()
        trade.join()

    except Exception as e:
        print(f"Fatal Error: {e}")


main()
