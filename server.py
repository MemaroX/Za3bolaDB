import socket
import threading
from engine import Za3bolaEngine

class Za3bolaServer:
    def __init__(self, host='127.0.0.1', port=8090):
        self.host = host
        self.port = port
        self.engine = Za3bolaEngine()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

    def handle_client(self, client_socket, addr):
        print(f"[+] New connection from {addr}")
        while True:
            try:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                response = self.process_command(data)
                client_socket.send(response.encode('utf-8'))
            except Exception as e:
                print(f"[!] Error: {e}")
                break
        
        print(f"[-] Connection closed from {addr}")
        client_socket.close()

    def process_command(self, command_str):
        parts = command_str.strip().split(' ', 2)
        cmd = parts[0].upper()

        if cmd == "SET":
            if len(parts) < 3:
                return "ERR: SET requires key and value"
            key, value = parts[1], parts[2]
            self.engine.set(key, value)
            return "OK"
        
        elif cmd == "GET":
            if len(parts) < 2:
                return "ERR: GET requires key"
            key = parts[1]
            val = self.engine.get(key)
            return str(val) if val is not None else "NULL"
        
        elif cmd == "DELETE":
            if len(parts) < 2:
                return "ERR: DELETE requires key"
            key = parts[1]
            if self.engine.delete(key):
                return "OK"
            return "ERR: Key not found"
        
        elif cmd == "LIST":
            keys = self.engine.list_keys()
            return ", ".join(keys) if keys else "EMPTY"
        
        elif cmd == "EXIT":
            return "BYE"
            
        return "ERR: Unknown command"

    def run(self):
        self.server_socket.listen(5)
        print(f"[*] Za3bolaDB Server listening on {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_thread.start()
        except KeyboardInterrupt:
            print("\n[*] Shutting down server...")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = Za3bolaServer()
    server.run()
