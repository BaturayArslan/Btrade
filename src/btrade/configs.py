from typing import List, Tuple, Optional, Union, Dict
from configparser import ConfigParser
from .exception import BadConfigOptions, BadFilePath
import os

ACCEPTED_CONFİG_FILE = {"secrets": ["key", "passphrase", "secret"]}


class Configs:
    def __init__(self):
        self._file_path: Optional[str] = None
        self.cparser = ConfigParser()

    def get_sections(self) -> List[str]:
        return self.cparser.sections()

    def get_section(self, section: str) -> List[Tuple[str, str]]:
        return self.cparser.items(section)

    def get(self, section: str, option: str) -> str:
        return self.cparser.get(section, option)

    def has_option(self, section: str, setting: str) -> bool:
        return self.cparser.has_option(section, setting)

    def set_file_path(self, file_path: str) -> None:
        if self._check_path(file_path):
            if not file_path.startswith("/"):
                current_directory = os.getcwd()
                absolute_path = os.path.join(current_directory, file_path)
                self._file_path = absolute_path
            else:
                self._file_path = file_path
            self.read()
        else:
            raise BadFilePath("File Doesnt Exist")

    def read(self):
        self.cparser.read(self._file_path)
        self._validate()

    def _validate(self):
        sections = self.get_sections()
        for section in sections:
            items = self.get_section(section)
            for key, value in items:
                if key not in ACCEPTED_CONFİG_FILE[section]:
                    raise BadConfigOptions(
                        f"You have Entered Unaccapted config file option ({key})")

    def _check_path(self, path: str) -> str:
        if path.startswith("/"):
            return os.path.isfile(path)
        else:
            current_directory = os.getcwd()
            absolute_path = os.path.join(current_directory, path)
            return os.path.isfile(absolute_path)

    def get_configs(self, options: List[Tuple[str, Union[str, int]]]) -> Dict:
        file_name = [option[1] for option in options if option[0] == "-f"]

        self.set_file_path(file_name[0])
        section = self.get_section("secrets")
        configs = {}
        for key, value in section:
            configs[key] = value
        return configs
