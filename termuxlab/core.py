from termuxlab.auth import AuthManager
from termuxlab.command_memory import CommandMemory
from termuxlab.logger_system import LoggerSystem
from termuxlab.monitor import SystemMonitor
from termuxlab.plugin_manager import PluginManager
from termuxlab.project_manager import ProjectManager
from termuxlab.report_generator import DailyReportGenerator
from termuxlab.scheduler import Scheduler
from termuxlab.session_tracker import SessionTracker
from termuxlab.terminal_control import TerminalControl
from termuxlab.utils import clear_screen, input_safe, yes_no


class LabSystem:
    def __init__(self):
        self.auth = AuthManager()
        self.logger = LoggerSystem()
        self.sessions = SessionTracker()
        self.commands = CommandMemory()
        self.monitor = SystemMonitor()
        self.projects = ProjectManager()
        self.scheduler = Scheduler()
        self.terminal = TerminalControl()
        self.plugins = PluginManager()
        self.reports = DailyReportGenerator()

    def startup(self):
        clear_screen()
        print("=== Termux Lab Logger — Portable Lab OS ===")
        if self.auth.is_locked() and not self.auth.authenticate():
            print("Authentication failed. Exiting.")
            return False
        return True

    def main_menu(self):
        print("\nMain Menu")
        print("1. Advanced Logging")
        print("2. Lab Session Tracker")
        print("3. AI Command Memory")
        print("4. Security & Authentication")
        print("5. System Monitor")
        print("6. Project Manager")
        print("7. Automation Scheduler")
        print("8. Terminal Control")
        print("9. Plugin Manager")
        print("10. Daily Report")
        print("0. Exit")

    def run(self):
        if not self.startup():
            return
        while True:
            self.main_menu()
            choice = input_safe("Select option: ").strip()
            if choice == "1":
                self.menu_logging()
            elif choice == "2":
                self.menu_sessions()
            elif choice == "3":
                self.menu_commands()
            elif choice == "4":
                self.menu_security()
            elif choice == "5":
                self.menu_monitor()
            elif choice == "6":
                self.menu_projects()
            elif choice == "7":
                self.menu_scheduler()
            elif choice == "8":
                self.menu_terminal()
            elif choice == "9":
                self.menu_plugins()
            elif choice == "10":
                self.menu_reports()
            elif choice == "0":
                print("Goodbye. Stay productive.")
                break
            else:
                print("Invalid choice.")

    def menu_logging(self):
        print("\nAdvanced Logging")
        print("1. Add log entry")
        print("2. View log entries")
        print("3. Search logs")
        choice = input_safe("Select option: ").strip()
        if choice == "1":
            title = input_safe("Title: ")
            category = input_safe("Category: ")
            tags = input_safe("Tags (comma-separated): ").split(",")
            note = input_safe("Entry note: ")
            result = input_safe("Result summary: ")
            entry = self.logger.add_entry(title, category, tags, note, result)
            print(f"Saved log entry: {entry.title}")
        elif choice == "2":
            entries = self.logger.list_entries()
            if not entries:
                print("No logs yet.")
                return
            for index, entry in enumerate(entries, start=1):
                print(f"\n[{index}] {entry['timestamp']} - {entry['title']} ({entry['category']})")
                print(f"  Tags: {', '.join(entry['tags'])}")
                print(f"  Note: {entry['note']}")
                print(f"  Result: {entry['result']}")
        elif choice == "3":
            keyword = input_safe("Search keyword: ")
            results = self.logger.search(keyword)
            for entry in results:
                print(f"- {entry['timestamp']} {entry['title']} [{entry['category']}]")
            if not results:
                print("No matching entries found.")
        else:
            print("Back to main menu.")

    def menu_sessions(self):
        print("\nLab Session Tracker")
        print("1. Start session")
        print("2. Stop session")
        print("3. View sessions")
        choice = input_safe("Select option: ").strip()
        if choice == "1":
            name = input_safe("Session name: ")
            project = input_safe("Project: ")
            notes = input_safe("Notes: ")
            session = self.sessions.start_session(name, project, notes)
            print(f"Session started: {session.name}")
        elif choice == "2":
            sessions = self.sessions.active_sessions()
            if not sessions:
                print("No active sessions.")
                return
            for index, session in enumerate(sessions, start=1):
                print(f"{index}. {session['name']} (Project: {session['project']})")
            selected = input_safe("Select session to stop: ").strip()
            if selected.isdigit():
                result = self.sessions.stop_session(int(selected) - 1)
                if result:
                    print("Session stopped.")
                else:
                    print("Could not stop the selected session.")
            else:
                print("Invalid value.")
        elif choice == "3":
            for index, session in enumerate(self.sessions.list_sessions(), start=1):
                status = "Active" if session["active"] else "Completed"
                print(f"{index}. {session['name']} [{status}] {session['start_time']} -> {session.get('end_time','')}" )
        else:
            print("Back to main menu.")

    def menu_commands(self):
        print("\nAI Command Memory")
        print("1. Remember command")
        print("2. View history")
        print("3. Search commands")
        choice = input_safe("Select option: ").strip()
        if choice == "1":
            command = input_safe("Command: ")
            context = input_safe("Context: ")
            tags = input_safe("Tags: ").split(",")
            record = self.commands.remember(command, context, tags)
            print(f"Saved command: {record.command}")
        elif choice == "2":
            for index, entry in enumerate(self.commands.history(), start=1):
                print(f"{index}. {entry['timestamp']} - {entry['command']} ({entry['context']})")
        elif choice == "3":
            query = input_safe("Search query: ")
            for entry in self.commands.search(query):
                print(f"- {entry['timestamp']}: {entry['command']} ({entry['context']})")
        else:
            print("Back to main menu.")

    def menu_security(self):
        print("\nSecurity & Authentication")
        if self.auth.is_locked():
            print("1. Change password")
            print("2. Disable password")
            choice = input_safe("Select option: ").strip()
            if choice == "1":
                self.auth.configure()
            elif choice == "2" and yes_no("Disable password protection?"):
                self.auth.store.save({})
                print("Password protection disabled.")
            else:
                print("Back to main menu.")
        else:
            print("1. Enable password")
            choice = input_safe("Select option: ").strip()
            if choice == "1":
                self.auth.configure()
            else:
                print("Back to main menu.")

    def menu_monitor(self):
        print("\nSystem Monitor")
        info = self.monitor.get_system()
        print(f"Snapshot: {info.get('snapshot')}")
        print(f"Load average: {info.get('load')}")
        disk = info.get("disk") or {}
        print(f"Disk: {disk.get('percent')}% used ({disk.get('free')} free)")
        mem = info.get("memory") or {}
        print(f"Memory: {mem.get('percent')}% used")

    def menu_projects(self):
        print("\nProject Manager")
        print("1. Create project")
        print("2. List projects")
        print("3. Add task")
        print("4. Toggle task complete")
        choice = input_safe("Select option: ").strip()
        if choice == "1":
            name = input_safe("Project name: ")
            description = input_safe("Description: ")
            self.projects.create_project(name, description)
            print("Project created.")
        elif choice == "2":
            for idx, project in enumerate(self.projects.list_projects(), start=1):
                print(f"{idx}. {project['name']} ({project['status']})")
                print(f"   {project['description']}")
                for task in project.get("tasks", []):
                    state = "✓" if task.get("completed") else "✗"
                    print(f"   - [{state}] {task['title']}")
        elif choice == "3":
            projects = self.projects.list_projects()
            for idx, project in enumerate(projects, start=1):
                print(f"{idx}. {project['name']}")
            selected = input_safe("Project number: ").strip()
            if selected.isdigit():
                task_title = input_safe("Task title: ")
                note = input_safe("Task note: ")
                self.projects.add_task(int(selected) - 1, task_title, note)
                print("Task added.")
        elif choice == "4":
            projects = self.projects.list_projects()
            for idx, project in enumerate(projects, start=1):
                print(f"{idx}. {project['name']}")
            project_select = input_safe("Project number: ").strip()
            if project_select.isdigit():
                project_index = int(project_select) - 1
                project = projects[project_index]
                for task_idx, task in enumerate(project.get("tasks", []), start=1):
                    status = "✓" if task.get("completed") else "✗"
                    print(f" {task_idx}. [{status}] {task['title']}")
                task_select = input_safe("Task number: ").strip()
                if task_select.isdigit():
                    self.projects.toggle_task(project_index, int(task_select) - 1)
                    print("Task toggled.")
        else:
            print("Back to main menu.")

    def menu_scheduler(self):
        print("\nAutomation Scheduler")
        print("1. Add scheduled task")
        print("2. View scheduled tasks")
        print("3. View due tasks")
        print("4. Mark task complete")
        choice = input_safe("Select option: ").strip()
        if choice == "1":
            title = input_safe("Task title: ")
            command = input_safe("Shell command: ")
            due_date = input_safe("Due date (YYYY-MM-DD HH:MM): ")
            note = input_safe("Note: ")
            self.scheduler.add_task(title, command, due_date, note)
            print("Scheduled task saved.")
        elif choice == "2":
            for index, task in enumerate(self.scheduler.list_tasks(), start=1):
                status = "Done" if task.get("completed") else "Pending"
                print(f"{index}. {task['title']} [{status}] - {task['due_date']}")
        elif choice == "3":
            for task in self.scheduler.due_tasks():
                print(f"- {task['title']} due {task['due_date']} ({task['command']})")
        elif choice == "4":
            tasks = self.scheduler.list_tasks()
            for index, task in enumerate(tasks, start=1):
                status = "Done" if task.get("completed") else "Pending"
                print(f"{index}. {task['title']} [{status}]")
            selected = input_safe("Task number: ").strip()
            if selected.isdigit():
                self.scheduler.mark_complete(int(selected) - 1)
                print("Task marked complete.")
        else:
            print("Back to main menu.")

    def menu_terminal(self):
        print("\nTerminal Control")
        print("1. Run shell command")
        print("2. Open shell session")
        print("3. List directory")
        choice = input_safe("Select option: ").strip()
        if choice == "1":
            command = input_safe("Command: ")
            self.terminal.run_command(command)
        elif choice == "2":
            self.terminal.shell_session()
        elif choice == "3":
            path = input_safe("Directory path: ") or "."
            self.terminal.list_directory(path)
        else:
            print("Back to main menu.")

    def menu_plugins(self):
        print("\nPlugin Manager")
        plugins = self.plugins.list_plugins()
        if not plugins:
            print("No plugins installed. Add Python files to the plugins/ folder.")
            return
        for index, plugin in enumerate(plugins, start=1):
            print(f"{index}. {plugin['name']} - {plugin['description']}")
        selected = input_safe("Run plugin number: ").strip()
        if selected.isdigit():
            if self.plugins.run_plugin(int(selected) - 1):
                print("Plugin executed.")
            else:
                print("Plugin execution failed.")

    def menu_reports(self):
        print("\nDaily Report")
        print(self.reports.generate())
