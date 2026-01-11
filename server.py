import socket
import threading
import json
import sys
import subprocess
import time
from engine import Za3bolaEngine

class Za3bolaServer:
    def __init__(self, host='127.0.0.1', port=8090, password='admin'):
        self.host = host
        self.port = port
        self.password = password
        self.engine = Za3bolaEngine()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.running = True

    def handle_client(self, client_socket, addr):
        print(f"[+] New connection from {addr}")
        authenticated = False
        current_table = 'default' # Default table for new connections
        
        while True:
            try:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                # Authentication Logic
                if not authenticated:
                    parts = data.strip().split(' ', 1)
                    if parts[0].upper() == "AUTH":
                        if len(parts) > 1 and parts[1] == self.password:
                            authenticated = True
                            client_socket.send("OK".encode('utf-8'))
                            continue
                        else:
                            client_socket.send("ERR: Invalid Password".encode('utf-8'))
                            break
                    else:
                        client_socket.send("ERR: Authentication Required".encode('utf-8'))
                        break

                # Process Command with Context
                response, new_table = self.process_command(data, current_table)
                
                # Update table if changed
                if new_table:
                    current_table = new_table
                
                client_socket.send(response.encode('utf-8'))
                
                if response == "SERVER_SHUTTING_DOWN":
                    break

            except Exception as e:
                print(f"[!] Error: {e}")
                break
        
        print(f"[-] Connection closed from {addr}")
        client_socket.close()

    def process_command(self, command_str, current_table):
        parts = command_str.strip().split(' ', 2)
        cmd = parts[0].upper()

        # --- USE Command ---
        if cmd == "USE":
            if len(parts) < 2:
                return "ERR: USE requires table name", None
            new_table_name = parts[1]
            return f"Switched to table '{new_table_name}'", new_table_name

        # --- SET / ADD / INSERT ---
        elif cmd in ["SET", "ADD", "INSERT"]:
            if len(parts) < 3:
                return "ERR: Command requires key and value", None
            key, value = parts[1], parts[2]
            
            try:
                parsed_value = json.loads(value)
                self.engine.set(current_table, key, parsed_value)
            except json.JSONDecodeError:
                self.engine.set(current_table, key, value)
            
            return "OK", None
        
        # --- GET ---
        elif cmd == "GET":
            # Check for GET ALL alias
            if len(parts) > 1 and parts[1].upper() == "ALL":
                return json.dumps(self.engine.get_all(current_table)), None
            
            if len(parts) < 2:
                return "ERR: GET requires key", None
            key = parts[1]
            val = self.engine.get(current_table, key)
            if val is None:
                return "NULL", None
            if isinstance(val, (dict, list)):
                return json.dumps(val), None
            return str(val), None
        
        # --- DELETE ---
        elif cmd in ["DELETE", "REMOVE"]:
            if len(parts) < 2:
                return "ERR: Command requires key", None
            key = parts[1]
            if self.engine.delete(current_table, key):
                return "OK", None
            return "ERR: Key not found", None
        
        # --- LIST ---
        elif cmd == "LIST":
            keys = self.engine.list_keys(current_table)
            return ", ".join(keys) if keys else "EMPTY", None
        
        # --- DUMP ---
        elif cmd == "DUMP":
            return json.dumps(self.engine.get_all(current_table)), None
        
        # --- HELP ---
        elif cmd == "HELP":
            return "COMMANDS: USE <table>, SET <k> <v>, GET <k>, GET ALL, DELETE <k>, LIST, SHUTDOWN", None
        
        # --- SYSTEM ---
        elif cmd == "SHUTDOWN":
            self.running = False
            return "SERVER_SHUTTING_DOWN", None
        
        elif cmd == "EXIT":
            return "BYE", None
            
        return "ERR: Unknown command. Type HELP for options.", None

    def run(self):
        self.server_socket.listen(5)
        self.server_socket.settimeout(1.0)
        print(f"[*] Za3bolaDB Server listening on {self.host}:{self.port}")
        
        try:
            while self.running:
                try:
                    client_socket, addr = self.server_socket.accept()
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                    client_thread.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\n[*] Shutting down server...")
        finally:
            print("[*] Server stopped.")
            self.server_socket.close()

def kill_process_on_port(port):
    print(f"[*] Attempting to terminate process on port {port}...")
    ps_cmd = f"Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue | ForEach-Object {{ Stop-Process -Id $_.OwningProcess -Force }}"
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True)
    time.sleep(1)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 8090
    
    try:
        server = Za3bolaServer(host=HOST, port=PORT)
        server.run()
    except OSError as e:
        if e.errno == 10048:
            print(f"[!] Port {PORT} is already in use.")
            try:
                choice = input("Do you want to terminate the existing server and restart? (y/n): ").strip().lower()
                if choice == 'y':
                    kill_process_on_port(PORT)
                    try:
                        print("[*] Restarting server...")
                        server = Za3bolaServer(host=HOST, port=PORT)
                        server.run()
                    except Exception as err:
                        print(f"[!] Failed to restart server: {err}")
                else:
                    print("[*] Startup aborted.")
            except KeyboardInterrupt:
                print("\n[*] Aborted.")
        else:
            raise e