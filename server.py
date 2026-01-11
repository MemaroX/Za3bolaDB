import socket
import threading
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

                response = self.process_command(data)
                client_socket.send(response.encode('utf-8'))
                
                if response == "SERVER_SHUTTING_DOWN":
                    break

            except Exception as e:
                print(f"[!] Error: {e}")
                break
        
        print(f"[-] Connection closed from {addr}")
        client_socket.close()

    def process_command(self, command_str):
        parts = command_str.strip().split(' ', 2)
        cmd = parts[0].upper()

        if cmd in ["SET", "ADD", "INSERT"]:
            if len(parts) < 3:
                return "ERR: Command requires key and value"
            key, value = parts[1], parts[2]
            self.engine.set(key, value)
            return "OK"
        
        elif cmd == "GET":
            if len(parts) < 2:
                return "ERR: GET requires key"
            key = parts[1]
            val = self.engine.get(key)
            return str(val) if val is not None else "NULL"
        
        elif cmd in ["DELETE", "REMOVE"]:
            if len(parts) < 2:
                return "ERR: Command requires key"
            key = parts[1]
            if self.engine.delete(key):
                return "OK"
            return "ERR: Key not found"
        
        elif cmd == "LIST":
            keys = self.engine.list_keys()
            return ", ".join(keys) if keys else "EMPTY"
        
        elif cmd == "HELP":
            return "COMMANDS: SET/ADD <k> <v>, GET <k>, DELETE/REMOVE <k>, LIST, SHUTDOWN, EXIT"
        
        elif cmd == "SHUTDOWN":
            self.running = False
            return "SERVER_SHUTTING_DOWN"
        
        elif cmd == "EXIT":
            return "BYE"
            
        return "ERR: Unknown command. Type HELP for options."

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

if __name__ == "__main__":
    server = Za3bolaServer()
    server.run()
