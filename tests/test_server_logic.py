import unittest
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import Za3bolaServer

class TestServerLogic(unittest.TestCase):
    def setUp(self):
        # Initialize server with port 0 (OS chooses free port) to avoid conflicts
        self.server = Za3bolaServer(port=0)
        # Manually clear engine data to keep tests isolated
        self.server.engine.data = {} 

    def test_json_handling(self):
        # Test INSERT with JSON
        json_str = '{"hero": "IronMan", "power": 100}'
        response = self.server.process_command(f"INSERT avenger {json_str}")
        self.assertEqual(response, "OK")
        
        # Verify it is stored as a dict in engine
        stored_val = self.server.engine.get("avenger")
        self.assertIsInstance(stored_val, dict)
        self.assertEqual(stored_val['hero'], "IronMan")

        # Test GET returns JSON string
        response = self.server.process_command("GET avenger")
        self.assertEqual(json.loads(response), json.loads(json_str))

    def test_process_set(self):
        response = self.server.process_command("SET name Za3bola")
        self.assertEqual(response, "OK")
        self.assertEqual(self.server.engine.get("name"), "Za3bola")

    def test_process_get(self):
        self.server.engine.set("lang", "Python")
        response = self.server.process_command("GET lang")
        self.assertEqual(response, "Python")
        
        response = self.server.process_command("GET missing")
        self.assertEqual(response, "NULL")

    def test_process_delete(self):
        self.server.engine.set("trash", "value")
        response = self.server.process_command("DELETE trash")
        self.assertEqual(response, "OK")
        self.assertIsNone(self.server.engine.get("trash"))

    def test_process_list(self):
        self.server.engine.set("k1", "v1")
        self.server.engine.set("k2", "v2")
        response = self.server.process_command("LIST")
        self.assertTrue("k1" in response and "k2" in response)

    def test_process_dump(self):
        self.server.engine.set("u1", "Maher")
        self.server.engine.set("u2", "Stark")
        
        # Test DUMP
        response = self.server.process_command("DUMP")
        data = json.loads(response)
        self.assertEqual(data['u1'], "Maher")
        self.assertEqual(data['u2'], "Stark")

        # Test GET ALL alias
        response_alias = self.server.process_command("GET ALL")
        self.assertEqual(response, response_alias)

    def test_process_invalid_command(self):
        response = self.server.process_command("DANCE")
        self.assertEqual(response, "ERR: Unknown command. Type HELP for options.")

if __name__ == '__main__':
    unittest.main()
