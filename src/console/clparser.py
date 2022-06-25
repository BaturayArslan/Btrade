from ctypes import Union
import getopt
import sys
import os
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
import pdb
import warnings
from collections import defaultdict

from requests import options
from exception import BadArgumentNumber, EmptyArgument, BadArgumentType, BadArgumentValue, BadFilePath, MissingArgument
from session import Session
from facade import Facade
from adapter import Adapter


ACCEPTED_SHORT_OPTIONS = "hl:p:s:e:f:"
ACCEPTED_LONG_OPTIONS = ["pair="]
ACCEPTED_EXCHANGES = ["kucoin", "binance"]


class Parser:

    def __init__(self) -> None:
        pass

    def parse(self, arguments):
        try:
            options, _ = getopt.getopt(
                arguments, ACCEPTED_SHORT_OPTIONS, ACCEPTED_LONG_OPTIONS)

            session = Session()
            self._validate(options, session)
            session.update(self._get_configs(options))
            self._set_api(session)
            return session

        except getopt.GetoptError as error:
            raise error
        except (BadArgumentNumber, BadArgumentType) as error:
            raise error
        except Exception as error:
            raise error

    def _validate(self, options: List[Tuple[str, Union[str, int]]], session: Dict) -> None:
        new_options = {}
        for option, value in options:
            if not option:
                raise EmptyArgument("You have entered one argument empty.")
            try:
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
            except Exception as e:
                raise e
        session.update(new_options)

    def _get_configs(self, options: List[Tuple[str, Union[str, int]]]) -> Dict:
        file_name = [option[1] for option in options if option[0] == "-f"]
        if not file_name:
            raise MissingArgument("You Have to provide -f argument.")
        Facade().settings.set_file_path(file_name[0])
        section = Facade().settings.get_section("secrets")
        configs = {}
        for key, value in section:
            configs[key] = value
        return configs

    def _set_api(self, session: Type[Session]):
        cls = self.import_wrapper(session["exchange"])
        obj = cls(session)
        session["api"] = Adapter(obj)

    def import_wrapper(self, exchange: str):
        module = __import__(f"wrappers.{exchange.lower()}", fromlist=[None])
        return getattr(module, f"{exchange.capitalize()}")
