import unittest
import socket
import threading
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import Za3bolaServer

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = '127.0.0.1'
        cls.port = 8092 # New port
        cls.password = 'testpass'
        cls.server = Za3bolaServer(host=cls.host, port=cls.port, password=cls.password)
        
        cls.server.engine.db_path = 'integration_test.aof'
        if os.path.exists(cls.server.engine.db_path):
            os.remove(cls.server.engine.db_path)

        cls.server_thread = threading.Thread(target=cls.server.run)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists('integration_test.aof'):
            os.remove('integration_test.aof')

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        return s

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