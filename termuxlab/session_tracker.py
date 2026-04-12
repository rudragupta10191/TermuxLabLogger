from dataclasses import dataclass, asdict
from datetime import datetime
from termuxlab.storage import JsonStore


@dataclass
class LabSession:
    name: str
    project: str
    notes: str
    start_time: str
    end_time: str
    active: bool


class SessionTracker:
    def __init__(self):
        self.store = JsonStore("sessions.json")

    def _current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def start_session(self, name, project, notes=""):
        session = LabSession(
            name=name,
            project=project,
            notes=notes,
            start_time=self._current_time(),
            end_time="",
            active=True,
        )
        self.store.append(asdict(session))
        return session

    def stop_session(self, index):
        sessions = self.store.load()
        if index < 0 or index >= len(sessions):
            return None
        session = sessions[index]
        if not session.get("active"):
            return session
        session["end_time"] = self._current_time()
        session["active"] = False
        self.store.replace(sessions)
        return session

    def list_sessions(self):
        return self.store.load()

    def active_sessions(self):
        return [session for session in self.list_sessions() if session.get("active")]
