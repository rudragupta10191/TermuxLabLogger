# TermuxLabLogger

**TermuxLabLogger** is a lightweight, modular lab operating system for Termux.
It is built for mobile-friendly use on Android via Termux, with offline support and a strong plugin architecture for future AI expansion.

---

## 🚀 System Features

- Advanced logging system with categories, tags, and searchable entries
- Lab session tracking for start/stop work logs
- AI command memory that stores and recalls shell command context
- Security authentication with optional password lock
- System monitoring for disk, load, and memory stats
- Project manager for tracking projects and tasks
- Automation scheduler for future reminders and command execution
- Terminal control commands and shell session integration
- Modular plugin architecture via `plugins/` folder
- Daily report generator with quick summaries

---

## 🧩 Architecture

- `logger.py` — main launcher for the Termux Lab Logger interface
- `termuxlab/` — core package with modular components
- `plugins/` — custom plugins can be added as Python scripts
- `.termuxlab/` — local storage folder for JSON data files

---

## 📥 Installation

```bash
pkg update && pkg upgrade
pkg install python git
cd /path/to/TermuxLabLogger
python logger.py
```

---

## ▶️ Usage

Run the system:

```bash
python logger.py
```

Navigate the menu to:

1. Add and search log entries
2. Track lab sessions
3. Remember commands
4. Secure the system with a password
5. Monitor the device
6. Manage projects and tasks
7. Schedule automation tasks
8. Run terminal commands
9. Load plugins from `plugins/`
10. Generate daily summaries

---

## 🔧 Create a Plugin

Add a Python file under `plugins/` with a `plugin_info` dictionary and a `run()` function.

Example:

```python
plugin_info = {
    "name": "Sample Lab Plugin",
    "description": "Demonstrates the Termux Lab Logger plugin system.",
}

def run():
    print("Sample plugin executed.")
```

---

## 📁 Notes

- No external packages are required.
- All data is stored locally in `~/.termuxlab/`.
- Designed to remain lightweight and extendable for future AI features.

