from watchdog.events import FileSystemEventHandler
import json
from queue import Queue
from typing import Type, Optional, Dict
from time import sleep


class MyEventHandler(FileSystemEventHandler):

    def __init__(self, que: Type[Queue]):
        FileSystemEventHandler.__init__(self)
        self.que = que
        self._event: Optional[Dict] = None

    def on_modified(self, event):
        if not event.is_directory:
            sleep(1)
            self.read_json(event.src_path)
            self.que.put(self._event)

    def read_json(self, path):
        with open(path, "r") as file:
            file_content = file.read()
            self._event = json.loads(file_content)
