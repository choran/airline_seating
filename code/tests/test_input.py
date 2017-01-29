import unittest
from lib.seat_assign_16200385_16201212_03783821 import Seating


class TestInput(unittest.TestCase):
    def test_even_sort(self):
        # Simple test list just to have test in framework
        input =  [7, 3, 4, 8, 1, 9, 14, 29, 0, -1, -8, -2]
        sorted_list = sorted(input, key=Seating.evens1st, reverse=True)
        result = [0, 4, 8, 14, 1, 3, 7, 9, 29, -1, -2, -8]
        self.assertEqual(sorted_list, result)



if __name__ == '__main__':
    unittest.main()
