from dataclasses import dataclass, asdict
from datetime import datetime
from termuxlab.storage import JsonStore


@dataclass
class ScheduledTask:
    title: str
    command: str
    due_date: str
    note: str
    completed: bool
    created_at: str


class Scheduler:
    def __init__(self):
        self.store = JsonStore("schedule.json")

    def add_task(self, title, command, due_date, note=""):
        task = ScheduledTask(
            title=title,
            command=command,
            due_date=due_date,
            note=note,
            completed=False,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self.store.append(asdict(task))
        return task

    def list_tasks(self):
        return self.store.load()

    def due_tasks(self):
        now = datetime.now()
        due = []
        for task in self.list_tasks():
            try:
                date = datetime.strptime(task["due_date"], "%Y-%m-%d %H:%M")
                if date <= now and not task.get("completed", False):
                    due.append(task)
            except ValueError:
                continue
        return due

    def mark_complete(self, index):
        tasks = self.list_tasks()
        if index < 0 or index >= len(tasks):
            return None
        tasks[index]["completed"] = True
        self.store.replace(tasks)
        return tasks[index]
