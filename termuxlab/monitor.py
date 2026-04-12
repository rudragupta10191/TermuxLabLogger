import os
import shutil
from termuxlab.utils import format_timestamp


class SystemMonitor:
    def __init__(self):
        self.timestamp = format_timestamp()

    def get_disk_usage(self, path="/"):
        try:
            usage = shutil.disk_usage(path)
            return {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": round(usage.used / usage.total * 100, 1) if usage.total else 0,
            }
        except Exception:
            return {}

    def get_load(self):
        if hasattr(os, "getloadavg"):
            averages = os.getloadavg()
            return {
                "1min": round(averages[0], 2),
                "5min": round(averages[1], 2),
                "15min": round(averages[2], 2),
            }
        return {}

    def get_memory(self):
        if os.path.exists("/proc/meminfo"):
            data = {}
            with open("/proc/meminfo", "r", encoding="utf-8") as file:
                for line in file:
                    key, value = line.split(":")[:2]
                    data[key.strip()] = int(value.strip().split()[0])
            total = data.get("MemTotal", 0)
            free = data.get("MemAvailable", data.get("MemFree", 0))
            used = total - free
            return {
                "total_kb": total,
                "used_kb": used,
                "available_kb": free,
                "percent": round(used / total * 100, 1) if total else 0,
            }
        return {}

    def get_system(self):
        return {
            "snapshot": self.timestamp,
            "load": self.get_load(),
            "disk": self.get_disk_usage(os.getcwd()),
            "memory": self.get_memory(),
        }
