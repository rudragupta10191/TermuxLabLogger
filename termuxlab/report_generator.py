from datetime import datetime
from termuxlab.storage import JsonStore


class DailyReportGenerator:
    def __init__(self):
        self.logs = JsonStore("logs.json")
        self.sessions = JsonStore("sessions.json")
        self.commands = JsonStore("commands.json")
        self.projects = JsonStore("projects.json")
        self.schedule = JsonStore("schedule.json")

    def generate(self):
        report_date = datetime.now().strftime("%Y-%m-%d")
        log_count = len(self.logs.load())
        session_count = len(self.sessions.load())
        command_count = len(self.commands.load())
        project_count = len(self.projects.load())
        task_count = sum(len(project.get("tasks", [])) for project in self.projects.load())
        due_tasks = len([task for task in self.schedule.load() if not task.get("completed")])

        report = [
            f"Termux Lab Logger Daily Report - {report_date}",
            "=" * 48,
            f"Total log entries    : {log_count}",
            f"Lab sessions tracked : {session_count}",
            f"Commands remembered   : {command_count}",
            f"Projects managed     : {project_count}",
            f"Project tasks total  : {task_count}",
            f"Pending schedule tasks: {due_tasks}",
            "",
            "Recent projects:",
        ]

        for project in self.projects.load()[-5:]:
            report.append(f"- {project.get('name')} ({project.get('status')})")

        return "\n".join(report)
