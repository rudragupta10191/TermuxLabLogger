from dataclasses import dataclass, asdict
from datetime import datetime
from termuxlab.storage import JsonStore
from termuxlab.utils import format_timestamp


@dataclass
class CommandRecord:
    command: str
    context: str
    tags: list
    timestamp: str


class CommandMemory:
    def __init__(self):
        self.store = JsonStore("commands.json")

    def remember(self, command, context="", tags=None):
        tags = tags or []
        record = CommandRecord(
            command=command,
            context=context,
            tags=[tag.strip() for tag in tags if tag.strip()],
            timestamp=format_timestamp(),
        )
        self.store.append(asdict(record))
        return record

    def history(self):
        return self.store.load()

    def search(self, query):
        query = query.lower()
        return [entry for entry in self.history() if query in entry["command"].lower() or query in entry["context"].lower()]
