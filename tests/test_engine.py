import unittest
import os
import sys
import json

# Add parent directory to path so we can import engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine import Za3bolaEngine

class TestZa3bolaEngine(unittest.TestCase):
    def setUp(self):
        self.test_db_path = 'test_data.json'
        # Ensure we start fresh
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.engine = Za3bolaEngine(db_path=self.test_db_path)

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_set_and_get(self):
        self.engine.set('user', 'Maher')
        self.assertEqual(self.engine.get('user'), 'Maher')
        self.assertIsNone(self.engine.get('nonexistent'))

    def test_delete(self):
        self.engine.set('temp', 'data')
        self.assertTrue(self.engine.delete('temp'))
        self.assertIsNone(self.engine.get('temp'))
        self.assertFalse(self.engine.delete('temp')) # Should fail second time

    def test_list_keys(self):
        self.engine.set('a', '1')
        self.engine.set('b', '2')
        keys = self.engine.list_keys()
        self.assertIn('a', keys)
        self.assertIn('b', keys)
        self.assertEqual(len(keys), 2)

    def test_nested_get(self):
        # Test Dot Notation
        data = {'user': {'profile': {'age': 30, 'city': 'NY'}}}
        self.engine.set('data', data)
        
        # Deep retrieval
        self.assertEqual(self.engine.get('data.user.profile.age'), 30)
        
        # Middle retrieval
        self.assertEqual(self.engine.get('data.user.profile'), {'age': 30, 'city': 'NY'})
        
        # Missing nested key
        self.assertIsNone(self.engine.get('data.user.profile.gender'))
        
        # Breaking the path (trying to go deep into a non-dict)
        self.assertIsNone(self.engine.get('data.user.profile.age.something'))

    def test_persistence(self):
        self.engine.set('persistent', 'value')
        # Create a new engine instance pointing to same file
        new_engine = Za3bolaEngine(db_path=self.test_db_path)
        self.assertEqual(new_engine.get('persistent'), 'value')

if __name__ == '__main__':
    unittest.main()
