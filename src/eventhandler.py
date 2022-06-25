from watchdog.events import FileSystemEventHandler
import json
from datetime import datetime


class MyEventHandler(FileSystemEventHandler):
    _event = None

    def on_modified(self, event):
        if not event.is_directory:
            self.read_json(event.src_path)

    def read_json(self, path):
        with open(path, "r") as file:
            file_content = file.read()
            self._event = json.loads(file_content)


event_handler = MyEventHandler()
