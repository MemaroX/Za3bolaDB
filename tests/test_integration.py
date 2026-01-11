import unittest
import socket
import threading
import time
import sys
import os
import ssl

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import Za3bolaServer
from tests.cert_helper import generate_test_certs, cleanup_test_certs

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert, cls.key = generate_test_certs()
        cls.host = '127.0.0.1'
        cls.port = 8092 
        cls.password = 'testpass'
        cls.server = Za3bolaServer(host=cls.host, port=cls.port, password=cls.password, certfile=cls.cert, keyfile=cls.key)
        
        cls.server.engine.db_path = 'integration_test.aof'
        if os.path.exists(cls.server.engine.db_path):
            os.remove(cls.server.engine.db_path)

        cls.server.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.server.running = False
        cleanup_test_certs(cls.cert, cls.key)
        if os.path.exists('integration_test.aof'):
            os.remove('integration_test.aof')

    def connect(self):
        # Create SSL Context (No verify for self-signed)
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_sock = context.wrap_socket(s, server_hostname=self.host)
        secure_sock.connect((self.host, self.port))
        return secure_sock

    def test_full_flow(self):
        s = self.connect()
        
        # Auth
        s.send(f"AUTH {self.password}".encode())
        self.assertEqual(s.recv(1024).decode(), "OK")
        
        # Use Table
        s.send(b"USE mytable")
        self.assertIn("Switched", s.recv(1024).decode())
        
        # Set Data
        s.send(b"SET key val")
        self.assertEqual(s.recv(1024).decode(), "OK")
        
        # Get Data
        s.send(b"GET key")
        self.assertEqual(s.recv(1024).decode(), "val")
        
        s.close()

if __name__ == '__main__':
    unittest.main()
