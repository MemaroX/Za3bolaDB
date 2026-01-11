import time
import socket
import threading
from server import Za3bolaServer

def run_demo():
    # 1. Initialize Server
    print("[Main] Initializing Za3bolaDB Server...")
    server = Za3bolaServer(port=8095) # Use a test port
    
    # 2. Start it (This would have blocked in the old version!)
    print("[Main] Calling server.start()...")
    server.start() 
    print("[Main] server.start() returned immediately! The main thread is free.")

    # 3. Do work in the main thread while server listens
    print("\n[Main] Starting background tasks...")
    for i in range(1, 4):
        print(f"[Main] doing heavy calculation {i}/3...")
        time.sleep(1)
        
        # At step 2, verify server is responsive
        if i == 2:
            print(f"\n   [Check] Connecting to server to prove it's listening...")
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', 8095))
                s.send(b"AUTH admin")
                response = s.recv(1024).decode()
                print(f"   [Check] Server responded: {response}")
                s.close()
                print(f"   [Check] Connection closed.\n")
            except Exception as e:
                print(f"   [Check] Failed: {e}")

    print("[Main] All tasks complete. Shutting down server.")
    server.running = False
    # In a real app, we'd wait for the thread to join, but for demo we just exit
    time.sleep(1) 

if __name__ == "__main__":
    run_demo()
