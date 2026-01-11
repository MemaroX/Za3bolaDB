import unittest
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import Za3bolaServer

class TestServerLogic(unittest.TestCase):
    def setUp(self):
        self.server = Za3bolaServer(port=0)
        self.server.engine.data = {'default': {}} 

    def test_use_command(self):
        # Default start
        current_table = 'default'
        
        # Switch table
        response, new_table = self.server.process_command("USE users", current_table)
        self.assertEqual(new_table, "users")
        self.assertIn("Switched to table", response)

    def test_data_isolation(self):
        # 1. Insert into 'users'
        self.server.process_command("USE users", 'default')
        self.server.process_command("SET name Maher", 'users')
        
        # 2. Insert into 'products'
        self.server.process_command("USE products", 'users')
        self.server.process_command("SET name Laptop", 'products')
        
        # 3. Verify 'users' has Maher
        resp, _ = self.server.process_command("GET name", 'users')
        self.assertEqual(resp, "Maher")
        
        # 4. Verify 'products' has Laptop
        resp, _ = self.server.process_command("GET name", 'products')
        self.assertEqual(resp, "Laptop")

    def test_json_handling(self):
        json_str = '{"hero": "IronMan"}'
        self.server.process_command(f"INSERT avenger {json_str}", 'default')
        
        resp, _ = self.server.process_command("GET avenger", 'default')
        self.assertEqual(json.loads(resp)['hero'], "IronMan")

    def test_dump(self):
        self.server.engine.set("default", "u1", "Maher")
        resp, _ = self.server.process_command("DUMP", "default")
        self.assertIn("Maher", resp)

if __name__ == '__main__':
    unittest.main()