from dataclasses import dataclass, asdict
from termuxlab.storage import JsonStore
from termuxlab.utils import format_timestamp


@dataclass
class LogEntry:
    title: str
    category: str
    tags: list
    note: str
    result: str
    timestamp: str


class LoggerSystem:
    def __init__(self):
        self.store = JsonStore("logs.json")

    def add_entry(self, title, category, tags, note, result):
        entry = LogEntry(
            title=title,
            category=category,
            tags=[tag.strip() for tag in tags if tag.strip()],
            note=note,
            result=result,
            timestamp=format_timestamp(),
        )
        self.store.append(asdict(entry))
        return entry

    def list_entries(self):
        return self.store.load()

    def search(self, keyword):
        keyword = keyword.lower()
        return [entry for entry in self.list_entries() if keyword in entry["title"].lower() or keyword in entry["note"].lower() or keyword in entry["category"].lower()]
