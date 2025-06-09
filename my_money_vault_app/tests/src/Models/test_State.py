import unittest
from src.Models.State import State

class test_State(unittest.TestCase):
    def test_new_1(self):
        state = State()
        state.account_id = 12
        state.balance = 112.33
        state.date = '2023-10-01 00:00:00'
        
        self.assertEqual(state.account_id, 12)
        self.assertEqual(state.balance, 112.33)
        self.assertEqual(state.date_string, '2023-10-01 00:00:00')
        
    def test_new_2(self):
        state = State()
        state.account_id = 2
        state.balance = 1022.00
        state.date = '2023-10-01 00:00:00'
        
        self.assertEqual(state.account_id, 2)
        self.assertEqual(state.balance, 1022.00)
        self.assertEqual(state.date_string, '2023-10-01 00:00:00')
        
    def test_new_constructor(self):
        state = State(account_id=3, balance=12.00)
        
        self.assertEqual(state.account_id, 3)
        self.assertEqual(state.balance, 12.00)
        
if __name__ == '__main__':
    unittest.main()
