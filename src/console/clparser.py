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
from exception import BadArgumentNumber, EmptyArgument, BadArgumentType, BadArgumentValue, BadFilePath
from session import Session
from facade import Facade


ACCEPTED_SHORT_OPTIONS = "hl:p:s:e:f:"
ACCEPTED_LONG_OPTIONS = ["pair="]
ACCEPTED_EXCHANGES = ["kucoin", "binance"]


class Parser:

    def __init__(self) -> None:
        pass

    def parse(self):
        try:
            arguments = sys.argv[1:]
            options, _ = getopt.getopt(
                arguments, ACCEPTED_SHORT_OPTIONS, ACCEPTED_LONG_OPTIONS)

            session = Session()
            self._validate(options, session)
            Facade().secrets

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
                elif option == "-f":
                    if self._check_path(value):
                        pass
                    else:
                        raise BadFilePath("File does not Exist.")
            except Exception as e:
                raise e
        session.update(new_options)

    def _check_path(self, path: str) -> str:
        if path.startswith("/"):
            return os.path.isfile(path)
        else:
            current_directory = os.getcwd()
            absolute_path = os.path.join(current_directory, path)
            return absolute_path
