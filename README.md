# Za3bolaDB

A high-performance, custom-built NoSQL Document Database.

## Features
- **In-Memory Speed**: Ultra-fast key-value operations with periodic disk persistence.
- **Document Store**: Full support for nested JSON objects and retrieval.
- **Deep Querying**: Access nested data using dot notation (e.g., `GET user.profile.email`).
- **Custom Protocol**: Lightweight TCP-based communication.
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
| `SET <key> <value>` | Store a value or JSON object. | `SET user {"name": "Stark"}` |
| `GET <key>` | Retrieve a value (supports nested keys). | `GET user.name` |
| `DELETE <key>` | Remove a key. | `DELETE user` |
| `LIST` | List all top-level keys. | `LIST` |
| `SHUTDOWN` | Remotely stop the server. | `SHUTDOWN` |
| `EXIT` | Disconnect from the server. | `EXIT` |

## Architecture
- **Server:** Multi-threaded TCP server handling concurrent connections.
- **Engine:** Python-based in-memory store with `json` serialization for persistence.
- **Security:** Basic password-based handshake protocol.

## License
MIT License