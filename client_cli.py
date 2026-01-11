import socket
import sys

def run_client(host='127.0.0.1', port=8090):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print(f"[*] Connected to Za3bolaDB at {host}:{port}")
        
        # Authentication
        pwd = input("Password: ")
        client_socket.send(f"AUTH {pwd}".encode('utf-8'))
        auth_response = client_socket.recv(4096).decode('utf-8')
        
        if auth_response != "OK":
            print(f"[-] Authentication failed: {auth_response}")
            client_socket.close()
            return

        print("[+] Authentication successful.")
        print("Type 'EXIT' to quit.")
        
        while True:
            cmd = input("Za3bolaDB > ")
            if not cmd:
                continue
            
            client_socket.send(cmd.encode('utf-8'))
            response = client_socket.recv(4096).decode('utf-8')
            print(response)
            
            if cmd.upper() == "EXIT" or response == "BYE" or response == "SERVER_SHUTTING_DOWN":
                break
                
    except ConnectionRefusedError:
        print("[!] Could not connect to the server. Is it running?")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_client()
