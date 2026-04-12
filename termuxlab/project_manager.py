from dataclasses import dataclass, asdict
from datetime import datetime
from termuxlab.storage import JsonStore


@dataclass
class Project:
    name: str
    description: str
    status: str
    created_at: str
    tasks: list


class ProjectManager:
    def __init__(self):
        self.store = JsonStore("projects.json")

    def create_project(self, name, description):
        project = Project(
            name=name,
            description=description,
            status="active",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tasks=[],
        )
        self.store.append(asdict(project))
        return project

    def list_projects(self):
        return self.store.load()

    def add_task(self, project_index, title, note=""):
        projects = self.list_projects()
        if project_index < 0 or project_index >= len(projects):
            return None
        task = {
            "title": title,
            "note": note,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        projects[project_index]["tasks"].append(task)
        self.store.replace(projects)
        return task

    def toggle_task(self, project_index, task_index):
        projects = self.list_projects()
        if project_index < 0 or project_index >= len(projects):
            return None
        project = projects[project_index]
        if task_index < 0 or task_index >= len(project["tasks"]):
            return None
        project["tasks"][task_index]["completed"] = not project["tasks"][task_index]["completed"]
        self.store.replace(projects)
        return project["tasks"][task_index]
