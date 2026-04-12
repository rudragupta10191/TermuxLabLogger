import hashlib
from termuxlab.storage import JsonStore


class AuthManager:
    def __init__(self):
        self.store = JsonStore("auth.json")
        self.config = self.store.load() or {}

    def _hash(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def set_password(self, password):
        self.config["password_hash"] = self._hash(password)
        self.store.save(self.config)

    def is_locked(self):
        return bool(self.config.get("password_hash"))

    def authenticate(self):
        if not self.is_locked():
            return True
        password = input("Enter system password: ")
        return self._hash(password) == self.config.get("password_hash")

    def configure(self):
        if self.is_locked():
            print("Security is already enabled.")
            return
        password = input("Set a new password: ")
        confirm = input("Confirm password: ")
        if password and password == confirm:
            self.set_password(password)
            print("✅ Password saved successfully.")
        else:
            print("⚠️ Passwords do not match or are empty.")
