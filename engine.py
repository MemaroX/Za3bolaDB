import json
import os

class Za3bolaEngine:
    def __init__(self, db_path='za3bola.aof'):
        self.db_path = db_path
        # Data structure: {'table_name': {'key': 'value'}}
        self.data = {'default': {}}
        self._recover_from_aof()

    def _recover_from_aof(self):
        """Replays the AOF log to rebuild the in-memory state."""
        if not os.path.exists(self.db_path):
            return

        print("[*] Replaying AOF log...")
        valid_lines = 0
        corrupt_lines = 0
        
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    line = line.strip()
                    if not line: continue
                    
                    try:
                        self._process_aof_line(line)
                        valid_lines += 1
                    except (ValueError, IndexError, json.JSONDecodeError) as e:
                        print(f"[!] Warning: Corrupt AOF line {i+1}: {e}")
                        corrupt_lines += 1
                        
        except Exception as e:
            print(f"[!] Critical Error recovering AOF: {e}")
            
        print(f"[*] Recovery complete. {valid_lines} valid, {corrupt_lines} corrupt.")

    def _process_aof_line(self, line):
        """Helper to parse a single AOF line."""
        parts = line.split(' ', 3)
        
        # New Format: CMD TABLE KEY [VALUE]
        if len(parts) >= 3:
            cmd = parts[0]
            
            if cmd == 'SET' and len(parts) == 4:
                _, table, key, val_json = parts
                if table not in self.data: self.data[table] = {}
                self.data[table][key] = json.loads(val_json)
                
            elif cmd == 'DEL':
                _, table, key = parts[:3]
                if table in self.data and key in self.data[table]:
                    del self.data[table][key]
                    
            # Legacy Format Support (CMD KEY [VALUE]) - assumes 'default' table
            elif cmd == 'SET' and len(parts) == 3:
                 _, key, val_json = parts
                 self.data['default'][key] = json.loads(val_json)
                 
            elif cmd == 'DEL' and len(parts) == 2:
                _, key = parts
                if key in self.data['default']:
                    del self.data['default'][key]

    def _append_aof(self, cmd, table, key, value=None):
        """Appends a command to the log file."""
        try:
            with open(self.db_path, 'a', encoding='utf-8') as f:
                if cmd == 'SET':
                    json_val = json.dumps(value)
                    f.write(f"SET {table} {key} {json_val}\n")
                elif cmd == 'DEL':
                    f.write(f"DEL {table} {key}\n")
        except Exception as e:
            print(f"[!] Error writing to AOF: {e}")

    def set(self, table, key, value):
        if table not in self.data:
            self.data[table] = {}
        self.data[table][key] = value
        self._append_aof('SET', table, key, value)
        return True

    def get(self, table, key):
        if table not in self.data:
            return None
            
        target_data = self.data[table]

        if '.' not in key:
            return target_data.get(key, None)
        
        # Nested access
        parts = key.split('.')
        current = target_data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current

    def delete(self, table, key):
        if table in self.data and key in self.data[table]:
            del self.data[table][key]
            self._append_aof('DEL', table, key)
            return True
        return False

    def list_keys(self, table):
        if table in self.data:
            return list(self.data[table].keys())
        return []

    def get_all(self, table):
        return self.data.get(table, {})

    def list_tables(self):
        return list(self.data.keys())
