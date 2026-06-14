import unittest
import socket
import time
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import Za3bolaServer
from tests.cert_helper import generate_test_certs, cleanup_test_certs

class TestEncryptionProof(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 1. Setup Secure Server
        cls.cert, cls.key = generate_test_certs()
        cls.port = 8099
        cls.server = Za3bolaServer(port=cls.port, certfile=cls.cert, keyfile=cls.key)
        cls.server.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.server.running = False
        cleanup_test_certs(cls.cert, cls.key)

    def test_spy_cannot_read_plaintext(self):
        """
        A raw TCP connection (Spy) trying to talk plaintext should fail 
        or receive binary TLS handshake packets, not readable text.
        """
        print("\n[Test] Launching Spy Connection (No SSL)...")
        spy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        spy.connect(('127.0.0.1', self.port))
        
        # Spy tries to send a command without SSL handshake
        msg = b"SET secret plaintext"
        spy.send(msg)
        
        try:
            # We expect either a connection close OR binary garbage (TLS handshake req)
            # We certainly do NOT expect "OK" or "ERR: Auth"
            response = spy.recv(1024)
            print(f"[Spy] Received: {response}")
            
            # If we received "OK" or a readable error, encryption is OFF.
            # If encryption is ON, the server expects a ClientHello (0x16), not "SET..."
            # It will likely close connection or ignore us.
            
            is_plaintext_response = b"OK" in response or b"ERR" in response
            self.assertFalse(is_plaintext_response, "Spy received plaintext response! Encryption is BROKEN.")
            
        except ConnectionResetError:
            print("[Spy] Connection forcibly closed by server (Good!)")
        
        spy.close()

if __name__ == "__main__":
    unittest.main()
