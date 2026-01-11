# Za3bolaDB (Security Branch)

A high-performance NoSQL Database with **SSL/TLS Encryption**.

## Features
- **Secure Communication**: All data is encrypted in transit using SSL/TLS.
- **Multi-Table Support**: Organize data into separate collections.
- **Append-Only Persistence**: Fast writes and crash recovery.
- **Remote Administration**: Built-in authentication and shutdown.

## Installation
```bash
git clone -b security https://github.com/MemaroX/Za3bolaDB.git
cd Za3bolaDB
```

## Security Setup (Required)
Before running the server, you must generate SSL certificates:
```bash
# Install cryptography (if not already installed)
pip install cryptography

# Run the generation script
python generate_cert.py
```
*(Note: You must create `generate_cert.py` or use your own certs named `server.crt` and `server.key`)*

## Quick Start
```bash
python server.py
python client_cli.py
```

## Architecture
- **Server:** SSL-wrapped TCP server.
- **Engine:** Python-based in-memory store.
- **Security:** SSL/TLS + Password Auth.

## License
MIT License