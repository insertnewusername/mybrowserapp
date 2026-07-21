import json
import os
from pathlib import Path

# Get the directory where this script is located
BASE_DIR = Path(__file__).parent

# Custom new-tab page: page.html (you can edit this file)
NEW_TAB_PAGE = BASE_DIR / "page.html"

# Convert to a file:// URL
if NEW_TAB_PAGE.exists():
    DEFAULT_URL = NEW_TAB_PAGE.as_uri()   # file:///path/to/page.html
else:
    # Fallback to Google if page.html doesn't exist
    DEFAULT_URL = "https://www.google.com"

class GroupManager:
    def __init__(self, storage_file="groups_data.json"):
        self.storage_file = storage_file
        self.groups = {}
        self.current_group = None
        self.load()

    def load(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, OSError):
                data = {}
        else:
            data = {}

        if isinstance(data, dict) and "groups" in data:
            self.groups = data.get("groups") or {}
            self.current_group = data.get("current_group")
        elif isinstance(data, dict) and data:
            # Legacy format: top-level keys are group names
            self.groups = data
            self.current_group = None
        else:
            self.groups = {}

        if not self.groups:
            self.groups = {"Default": [DEFAULT_URL]}

        self._normalize_urls()

        if not self.current_group or self.current_group not in self.groups:
            self.current_group = list(self.groups.keys())[0]

    def _normalize_urls(self):
        for name, urls in list(self.groups.items()):
            if not urls:
                self.groups[name] = [DEFAULT_URL]
                continue
            self.groups[name] = [
                DEFAULT_URL if url in ("about:blank", "") else url for url in urls
            ]

    def save(self):
        data = {
            "current_group": self.current_group,
            "groups": self.groups,
        }
        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=2)

    def add_group(self, name):
        name = name.strip()
        if not name or name in self.groups:
            return False
        self.groups[name] = [DEFAULT_URL]
        self.current_group = name
        self.save()
        return True

    def delete_group(self, name):
        if len(self.groups) <= 1:
            return False
        if name in self.groups:
            del self.groups[name]
            if self.current_group == name:
                self.current_group = list(self.groups.keys())[0]
            self.save()
            return True
        return False

    def rename_group(self, old_name, new_name):
        new_name = new_name.strip()
        if not new_name or new_name in self.groups or old_name not in self.groups:
            return False
        self.groups[new_name] = self.groups.pop(old_name)
        if self.current_group == old_name:
            self.current_group = new_name
        self.save()
        return True

    def get_urls(self, group_name):
        urls = self.groups.get(group_name)
        if not urls:
            return [DEFAULT_URL]
        return urls

    def set_urls(self, group_name, urls):
        if group_name in self.groups:
            self.groups[group_name] = urls or [DEFAULT_URL]
            self.save()

    def group_names(self):
        return list(self.groups.keys())
