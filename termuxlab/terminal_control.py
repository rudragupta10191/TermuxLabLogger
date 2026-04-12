import subprocess
from termuxlab.utils import input_safe


class TerminalControl:
    def run_command(self, command):
        print(f"Running: {command}")
        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            print("--- Output ---")
            print(result.stdout or "(no output)")
            if result.stderr:
                print("--- Errors ---")
                print(result.stderr)
            return result.returncode
        except Exception as exc:
            print(f"Command failed: {exc}")
            return -1

    def shell_session(self):
        print("Enter commands to run. Type 'exit' to leave.")
        while True:
            command = input_safe("termux> ")
            if not command or command.lower() == "exit":
                break
            self.run_command(command)

    def list_directory(self, path="."):
        try:
            files = subprocess.check_output(["ls", "-la", path], text=True)
            print(files)
        except Exception as exc:
            print(f"Unable to list directory: {exc}")
