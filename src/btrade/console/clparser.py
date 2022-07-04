from ctypes import Union
import getopt
import sys
from importlib import import_module
from operator import length_hint
from typing import (
    List,
    Any,
    Type,
    Optional,
    Tuple,
    Set,
    Dict,
    Union
)

from ..exception import BadArgumentNumber, EmptyArgument, BadArgumentType, BadArgumentValue, BadFilePath, MissingArgument
from ..session import Session
from ..facade import Facade
from ..adapter import Adapter
from .. import wrappers

ACCEPTED_SHORT_OPTIONS = "hl:p:s:e:f:"
ACCEPTED_LONG_OPTIONS = ["pair=", "help"]
ACCEPTED_EXCHANGES = ["kucoin", "binance"]


class Parser:

    def __init__(self) -> None:
        pass

    def parse(self, arguments) -> Type[Session]:
        try:
            options, _ = getopt.getopt(
                arguments, ACCEPTED_SHORT_OPTIONS, ACCEPTED_LONG_OPTIONS)
            self.show_help(arguments)

            session = Session()
            self._validate(options, session)
            configs = Facade().settings.get_configs(options)
            session.update(configs)
            self._set_api(session)
            return session

        except Exception as error:
            raise error

    def _validate(self, options: List[Tuple[str, Union[str, int]]], session: Dict) -> None:
        new_options = {}
        try:
            if not len(options) == 6:
                raise BadArgumentNumber(
                    "You Have entered wrong number of argument.")
            for option, value in options:
                if not value:
                    raise EmptyArgument(
                        f"You have entered {option} argument empty.")
                if option == "-p":
                    new_options["profit_trashold"] = int(value)
                elif option == "-s":
                    new_options["loss_trashold"] = int(value)
                elif option == "-l":
                    new_options["leverage"] = int(value)
                elif option == "--pair":
                    new_options["pair"] = value
                elif option == "-e":
                    if value in ACCEPTED_EXCHANGES:
                        new_options["exchange"] = value
                    else:
                        raise BadArgumentValue(
                            "You Have Entered Bad Unacceptable Argment value.")
        except ValueError as e:
            self.show_usage()
            raise BadArgumentType("Type Error. Wrong argument type.")
        except Exception as e:
            self.show_usage()
            raise e

        session.update(new_options)

    def _set_api(self, session: Type[Session]):
        cls = self.import_wrapper(session["exchange"])
        obj = cls(session)
        session["api"]: Type[Adapter] = Adapter(obj)

    def import_wrapper(self, exchange: str):
        module = import_module(f".wrappers.{exchange.lower()}", "btrade")
        return getattr(module, f"{exchange.capitalize()}")

    def show_usage(self):
        print(
            "Usage:: btrade -l 10 -p 30 -s 15 -e kucoin --pair 'XBTUSDM' -f ./config.ini")

    def show_banner(self):
        banner = '''*****************************************************
* Btrade - Automation For Future Trading{allign: <{width}} *
* Created By Baturay Arslan{allign: <{width2}} * 
*****************************************************
        '''.format(width=11, allign=" ", width2=24)
        print(banner)

    def show_options(self):
        pass

    def show_help(self, options: List[str]) -> None:
        if "-h" in options or "--help" in options:
            self.show_banner()
            self.show_usage()
            self.show_options()
            sys.exit(-1)
