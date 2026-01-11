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
        # Start server in a background thread
        cls.host = '127.0.0.1'
        cls.port = 8091 # Use a different port for testing
        cls.password = 'testpass'
        cls.server = Za3bolaServer(host=cls.host, port=cls.port, password=cls.password)
        
        # Override engine path to avoid messing with main data
        cls.server.engine.db_path = 'integration_test_data.json'
        if os.path.exists(cls.server.engine.db_path):
            os.remove(cls.server.engine.db_path)

        cls.server_thread = threading.Thread(target=cls.server.run)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1) # Give server time to start

    @classmethod
    def tearDownClass(cls):
        # Cleanup
        if os.path.exists('integration_test_data.json'):
            os.remove('integration_test_data.json')

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        return s

    def test_auth_success(self):
        s = self.connect()
        s.send(f"AUTH {self.password}".encode())
        resp = s.recv(1024).decode()
        self.assertEqual(resp, "OK")
        
        s.send(b"SET key val")
        resp = s.recv(1024).decode()
        self.assertEqual(resp, "OK")
        s.close()

    def test_auth_fail(self):
        s = self.connect()
        s.send(b"AUTH wrongpass")
        resp = s.recv(1024).decode()
        self.assertEqual(resp, "ERR: Invalid Password")
        # Connection should be closed by server
        data = s.recv(1024)
        self.assertEqual(data, b"") 
        s.close()

    def test_command_without_auth(self):
        s = self.connect()
        s.send(b"SET hacker try")
        resp = s.recv(1024).decode()
        self.assertEqual(resp, "ERR: Authentication Required")
        s.close()

if __name__ == '__main__':
    unittest.main()
