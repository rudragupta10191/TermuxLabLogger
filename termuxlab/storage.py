import json
import os
from pathlib import Path

DEFAULT_FOLDER = Path.home() / ".termuxlab"
DEFAULT_FOLDER.mkdir(parents=True, exist_ok=True)


class JsonStore:
    def __init__(self, filename):
        self.path = DEFAULT_FOLDER / filename
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self):
        if not self.path.exists():
            return []
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def append(self, item):
        data = self.load()
        data.append(item)
        self.save(data)

    def replace(self, data):
        self.save(data)
