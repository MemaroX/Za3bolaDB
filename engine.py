import json
import os

class Za3bolaEngine:
    def __init__(self, db_path='za3bola.aof'):
        self.db_path = db_path
        self.data = {}
        self._recover_from_aof()

    def _recover_from_aof(self):
        """Replays the AOF log to rebuild the in-memory state."""
        if not os.path.exists(self.db_path):
            return

        print("[*] Replaying AOF log...")
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    
                    try:
                        parts = line.split(' ', 2)
                        cmd = parts[0]
                        
                        if cmd == 'SET':
                            key = parts[1]
                            val_json = parts[2]
                            self.data[key] = json.loads(val_json)
                        elif cmd == 'DEL':
                            key = parts[1]
                            if key in self.data:
                                del self.data[key]
                    except Exception:
                        continue # Skip corrupted lines
        except Exception as e:
            print(f"[!] Error recovering AOF: {e}")
        print("[*] Recovery complete.")

    def _append_aof(self, cmd, key, value=None):
        """Appends a command to the log file."""
        try:
            with open(self.db_path, 'a', encoding='utf-8') as f:
                if cmd == 'SET':
                    # Serialize value to JSON to ensure it fits on one line and handles special chars
                    json_val = json.dumps(value)
                    f.write(f"SET {key} {json_val}\n")
                elif cmd == 'DEL':
                    f.write(f"DEL {key}\n")
        except Exception as e:
            print(f"[!] Error writing to AOF: {e}")

    def set(self, key, value):
        self.data[key] = value
        self._append_aof('SET', key, value)
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
            self._append_aof('DEL', key)
            return True
        return False

    def list_keys(self):
        return list(self.data.keys())