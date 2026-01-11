import unittest
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine import Za3bolaEngine

class TestZa3bolaEngine(unittest.TestCase):
    def setUp(self):
        self.test_db_path = 'test_data.aof'
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.engine = Za3bolaEngine(db_path=self.test_db_path)

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_set_and_get_default(self):
        self.engine.set('default', 'user', 'Maher')
        self.assertEqual(self.engine.get('default', 'user'), 'Maher')

    def test_table_isolation(self):
        # Set 'key' in 'table1'
        self.engine.set('table1', 'key', 'val1')
        # Set same 'key' in 'table2'
        self.engine.set('table2', 'key', 'val2')
        
        self.assertEqual(self.engine.get('table1', 'key'), 'val1')
        self.assertEqual(self.engine.get('table2', 'key'), 'val2')

    def test_delete(self):
        self.engine.set('default', 'temp', 'data')
        self.assertTrue(self.engine.delete('default', 'temp'))
        self.assertIsNone(self.engine.get('default', 'temp'))

    def test_list_keys(self):
        self.engine.set('t1', 'a', '1')
        self.engine.set('t1', 'b', '2')
        keys = self.engine.list_keys('t1')
        self.assertIn('a', keys)
        self.assertIn('b', keys)
        self.assertEqual(len(keys), 2)
        
        # Ensure t2 is empty
        self.assertEqual(len(self.engine.list_keys('t2')), 0)

    def test_nested_get(self):
        data = {'profile': {'age': 30}}
        self.engine.set('users', 'maher', data)
        self.assertEqual(self.engine.get('users', 'maher.profile.age'), 30)

    def test_persistence(self):
        self.engine.set('t1', 'persistent', 'value')
        
        # Create new engine to simulate restart
        new_engine = Za3bolaEngine(db_path=self.test_db_path)
        self.assertEqual(new_engine.get('t1', 'persistent'), 'value')

if __name__ == '__main__':
    unittest.main()