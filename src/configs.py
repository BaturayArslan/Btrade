from typing import List, Tuple, Optional
from configparser import ConfigParser


class Configs:
    def __init__(self):
        self._file_name: Optional[str] = None
        self.cparser = ConfigParser()

    def get_sections(self) -> List[str]:
        return self.cparser.sections

    def get_section(self, section: str) -> List[Tuple[str, str]]:
        return self.cparser.items(section)

    def get(self, section: str, option: str) -> str:
        return self.cparser.get(section, option)

    def has_option(self, section: str, setting: str) -> bool:
        return self.cparser.has_option(section, setting)

    def set_file_name(self, file_name: str) -> None:
        self._file_name = file_name
        self.read()

    def read(self):
        self.cparser.read(self._file_name)
