import socket
import sys
import ssl
import re
import json
from colorama import init, Fore, Style

# Try to import readline for history support
try:
    import readline
except ImportError:
    try:
        import pyreadline3 as readline
    except ImportError:
        readline = None

# Initialize colorama
init(autoreset=True)

# Re-engineered robust banner
B_CYAN = Fore.CYAN + Style.BRIGHT
RESET = Style.RESET_ALL
WHITE = Fore.WHITE

BANNER = f"""{B_CYAN}
  _____        ____  _           _       _____  ____  
 |__  /__ _ __| __ )| | ___ __ _| |__   |  __ \| __ ) 
   / / _` |_  /  _ \| |/ _ \ _` | '_ \  | |  | |  _ \ 
  / / (_| |/ /| |_) | | (_) (_| | |_) | | |__| | |_) |
 /___\__,_/___|____/|_|\___|__,_|_.__/  |_____/|____/ 
{RESET}      {WHITE}The Secure NoSQL Engine | v1.3 | @MemaroX
"""

class Za3bolaCompleter:
    def __init__(self):
        self.commands = [
            "SET", "GET", "DELETE", "LIST", "DUMP", "USE", "HELP", "EXIT", 
            "SHUTDOWN", "TABLES", "AUTH", "ADD", "INSERT", "REMOVE"
        ]
        self.tables = ["default"]

    def complete(self, text, state):
        buffer = readline.get_line_buffer().upper()
        options = []

        if "USE " in buffer:
            # Autocomplete tables
            options = [t for t in self.tables if t.upper().startswith(text.upper())]
        else:
            # Autocomplete commands
            options = [c for c in self.commands if c.startswith(text.upper())]
        
        if state < len(options):
            return options[state]
        return None

    def add_table(self, table_name):
        if table_name not in self.tables:
            self.tables.append(table_name)

def run_client(host='127.0.0.1', port=8090):
    print(BANNER)
    
    # SSL Context Setup (Secure Mode)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    current_table = "default"
    
    # Setup Autocomplete
    completer = Za3bolaCompleter()
    if readline:
        readline.set_completer(completer.complete)
        readline.parse_and_bind("tab: complete")

    try:
        # Connect Securely
        client_socket = context.wrap_socket(raw_socket, server_hostname=host)
        client_socket.connect((host, port))
        
        print(f"{Fore.BLUE}[*] Securely connected to Za3bolaDB at {host}:{port}")
        
        pwd = input(f"{Fore.YELLOW}Password: {Style.RESET_ALL}")
        client_socket.send(f"AUTH {pwd}".encode('utf-8'))
        auth_response = client_socket.recv(4096).decode('utf-8')
        
        if auth_response != "OK":
            print(f"{Fore.RED}[-] Authentication failed: {auth_response}")
            client_socket.close()
            return

        print(f"{Fore.GREEN}[+] Authentication successful.")
        print(f"{Fore.WHITE}Type 'HELP' for commands or 'EXIT' to quit.")
        
        # Initial fetch of tables for autocompleter
        client_socket.send(b"TABLES")
        tables_resp = client_socket.recv(4096).decode('utf-8')
        if tables_resp and "ERR" not in tables_resp:
            for t in tables_resp.split(", "):
                completer.add_table(t)
        
        while True:
            try:
                # Dynamic Prompt showing current table
                prompt = f"\n{Fore.MAGENTA}Za3bolaDB {Fore.CYAN}[{current_table}] {Fore.WHITE}> {Style.RESET_ALL}"
                cmd = input(prompt).strip()
                
                if not cmd:
                    continue
                
                # Update completer if we switch tables or add new ones
                if cmd.upper().startswith("USE "):
                    parts = cmd.split(" ")
                    if len(parts) > 1:
                        completer.add_table(parts[1])

                client_socket.send(cmd.encode('utf-8'))
                response = client_socket.recv(4096).decode('utf-8')
                
                # Update current table context if switched
                if "Switched to table" in response:
                    match = re.search(r"'(.*?)'", response)
                    if match:
                        current_table = match.group(1)

                # Stylish response handling
                if response.startswith("ERR:"):
                    print(f"{Fore.RED}{response}")
                elif response == "OK":
                    print(f"{Fore.GREEN}{response}")
                elif response == "NULL":
                    print(f"{Fore.YELLOW}{response}")
                elif response.startswith("{based on the provided context, the following changes were made:") or response.startswith("["):
                    # Pretty print JSON if possible
                    try:
                        parsed = json.loads(response)
                        print(f"{Fore.CYAN}{json.dumps(parsed, indent=4)}")
                    except:
                        print(f"{Fore.CYAN}{response}")
                else:
                    print(f"{Fore.CYAN}{response}")
                
                if cmd.upper() == "EXIT" or response == "BYE" or response == "SERVER_SHUTTING_DOWN":
                    if response == "SERVER_SHUTTING_DOWN":
                        print(f"{Fore.YELLOW}[!] Server is shutting down...")
                    print(f"{Fore.WHITE}Goodbye.")
                    break
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[*] Disconnecting...")
                break
                
    except ConnectionRefusedError:
        print(f"{Fore.RED}[!] Could not connect to the server. Is it running in SECURE mode?")
    except ssl.SSLError as e:
        print(f"{Fore.RED}[!] SSL Connection Error: {e}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_client()