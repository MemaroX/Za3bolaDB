import json
import os

class Za3bolaEngine:
    def __init__(self, db_path='data.json'):
        self.db_path = db_path
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def set(self, key, value):
        self.data[key] = value
        self.save()
        return True

    def get(self, key):
        if '.' not in key:
            return self.data.get(key, None)
        
        # Nested access (e.g., "user.profile.name")
        parts = key.split('.')
        current = self.data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self.save()
            return True
        return False

    def list_keys(self):
        return list(self.data.keys())
