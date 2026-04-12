import importlib.util
import os
from pathlib import Path
from termuxlab.utils import ensure_directory


PLUGIN_FOLDER = Path.cwd() / "plugins"
ensure_directory(PLUGIN_FOLDER)


class PluginManager:
    def __init__(self):
        self.plugins = []
        self.load_plugins()

    def load_plugins(self):
        self.plugins = []
        for plugin_file in PLUGIN_FOLDER.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue
            spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                metadata = getattr(module, "plugin_info", {})
                runner = getattr(module, "run", None)
                if runner:
                    self.plugins.append({"name": metadata.get("name", plugin_file.stem), "description": metadata.get("description", ""), "module": module, "run": runner})
            except Exception:
                continue

    def list_plugins(self):
        return self.plugins

    def run_plugin(self, index):
        if index < 0 or index >= len(self.plugins):
            return False
        try:
            self.plugins[index]["run"]()
            return True
        except Exception as exc:
            print(f"Plugin failed: {exc}")
            return False
