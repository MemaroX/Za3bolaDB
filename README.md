# Za3bolaDB

A high-performance, secure, multi-threaded NoSQL Document Database.

## Features
- **Secure Communication**: Full SSL/TLS encryption for all data in transit.
- **Multi-Threaded Architecture**: Non-blocking background server processing.
- **Append-Only Persistence**: O(1) write performance and robust crash recovery via AOF logs.
- **Multi-Table Support**: Organize data into logical collections (e.g., `USE users`).
- **Document Store**: Store and retrieve nested JSON objects.
- **Deep Querying**: Access nested data using dot notation (e.g., `GET user.profile.email`).
- **Advanced UX**: Interactive CLI with colors, ASCII banner, and tab autocompletion.
- **Remote Administration**: Secure authentication and remote shutdown capabilities.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/MemaroX/Za3bolaDB.git
cd Za3bolaDB
```

### 2. Install Dependencies
```bash
pip install cryptography colorama pyreadline3
```

### 3. Generate Security Certificates
```bash
python generate_cert.py
```

## Quick Start

### Start the Server
```bash
python server.py
# Default Port: 8090 | Default Password: admin
```

### Connect with the CLI
```bash
python client_cli.py
```

## Command Reference

| Command | Description | Example |
| :--- | :--- | :--- |
| `AUTH <password>` | Authenticate with the server. | `AUTH admin` |
| `USE <table>` | Switch the active collection/table. | `USE users` |
| `TABLES` | List all available tables. | `TABLES` |
| `SET <k> <v>` | Store a value or JSON object. | `SET u1 {"name": "Maher"}` |
| `GET <k>` | Retrieve a value (supports dot-notation). | `GET u1.name` |
| `DUMP [t]` | Retrieve all data from current or target table. | `DUMP products` |
| `GET ALL [t]` | Alias for DUMP. | `GET ALL` |
| `DELETE <k>` | Remove a key from the current table. | `DELETE u1` |
| `LIST [t]` | List keys in current or target table. | `LIST` |
| `SHUTDOWN` | Remotely stop the server. | `SHUTDOWN` |
| `EXIT` | Disconnect from the server. | `EXIT` |

## Technical Architecture
- **Server:** Multi-threaded TCP server utilizing `ssl` for secure handshakes and `threading` for concurrent client management.
- **Engine:** In-memory storage with an Append-Only File (AOF) log for transactional durability.
- **CLI:** Enhanced with `colorama` for visual feedback and `readline` for command history and autocompletion.

## License
MIT License | Built with precision by @MemaroX
