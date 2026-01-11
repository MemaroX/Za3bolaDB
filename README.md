# Za3bolaDB

A high-performance, custom-built NoSQL Document Database with Multi-Collection support.

## Features
- **Multi-Table Support**: Organize data into separate collections (e.g., `USE users`).
- **Append-Only Persistence**: Fast writes and crash recovery using AOF logs.
- **In-Memory Speed**: Ultra-fast key-value operations.
- **Document Store**: Full support for nested JSON objects and retrieval.
- **Deep Querying**: Access nested data using dot notation (e.g., `GET user.profile.email`).
- **Remote Administration**: Built-in authentication and shutdown commands.

## Installation
```bash
git clone https://github.com/MemaroX/Za3bolaDB.git
cd Za3bolaDB
```

## Quick Start

### 1. Start the Server
```bash
python server.py
# Default Port: 8090
# Default Password: admin
```

### 2. Connect with CLI
```bash
python client_cli.py
```

## Command Reference

| Command | Description | Example |
| :--- | :--- | :--- |
| `AUTH <password>` | Authenticate with the server. | `AUTH admin` |
| `USE <table>` | Switch to a specific table/collection. | `USE users` |
| `SET <key> <value>` | Store a value or JSON object in current table. | `SET user {"name": "Stark"}` |
| `GET <key>` | Retrieve a value (supports nested keys). | `GET user.name` |
| `GET ALL` / `DUMP` | Retrieve all data in the current table. | `DUMP` |
| `DELETE <key>` | Remove a key from current table. | `DELETE user` |
| `LIST` | List all keys in current table. | `LIST` |
| `SHUTDOWN` | Remotely stop the server. | `SHUTDOWN` |
| `EXIT` | Disconnect from the server. | `EXIT` |

## Architecture
- **Server:** Multi-threaded TCP server handling concurrent connections.
- **Engine:** Python-based in-memory store with Append-Only File (AOF) persistence.
- **Security:** Basic password-based handshake protocol.

## License
MIT License
