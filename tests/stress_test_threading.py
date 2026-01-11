import threading
import socket
import time
import random
from server import Za3bolaServer

# Configuration
CLIENT_COUNT = 50
PORT = 8096
HOST = '127.0.0.1'

def client_task(client_id):
    """Simulates a single client performing operations."""
    try:
        # Random delay to simulate real-world chaos
        time.sleep(random.uniform(0.1, 0.5))
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        
        # 1. Auth
        s.send(b"AUTH admin")
        if s.recv(1024).decode() != "OK":
            print(f"[Client {client_id}] Auth Failed!")
            return

        # 2. Write Data
        key = f"user_{client_id}"
        val = f"data_{client_id}"
        s.send(f"SET {key} {val}".encode())
        resp = s.recv(1024).decode()
        
        # 3. Read Data
        s.send(f"GET {key}".encode())
        read_val = s.recv(1024).decode()
        
        if read_val == val:
            print(f"[Client {client_id}] SUCCESS (Wrote/Read: {val})")
        else:
            print(f"[Client {client_id}] FAIL! Expected {val}, got {read_val}")
            
        s.close()
    except Exception as e:
        print(f"[Client {client_id}] CRASH: {e}")

def run_stress_test():
    print(f"[*] Starting Hardcore Threading Test with {CLIENT_COUNT} concurrent clients...")
    
    # Start Server
    server = Za3bolaServer(port=PORT)
    server.start()
    
    # Spawn Clients
    threads = []
    start_time = time.time()
    
    for i in range(CLIENT_COUNT):
        t = threading.Thread(target=client_task, args=(i,))
        threads.append(t)
        t.start()
        
    # Wait for all to finish
    for t in threads:
        t.join()
        
    duration = time.time() - start_time
    print(f"[*] Test Complete in {duration:.2f} seconds.")
    
    # Verify final state
    print(f"[*] Server Final Key Count: {len(server.engine.list_keys('default'))}")
    
    # Shutdown
    server.running = False

if __name__ == "__main__":
    run_stress_test()
