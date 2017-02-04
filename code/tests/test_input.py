import unittest
from lib.seat_assign import Seating


class TestInput(unittest.TestCase):
    def test_even_sort(self):
        # Simple test list just to have test in framework
        # input =  [7, 3, 4, 8, 1, 9, 14, 29, 0, -1, -8, -2]
        input = {'1': 7, '2': 3, '4': 4, '5': 8, '6': 1, '7': 9, '8': 14,
                  '9': 29, '10': 0, '11': -1, '12': -8, '13': -2}
        sorted_list = sorted(input.items(), key=Seating.evens1st, reverse=True)
        result = [('10', 0), ('4', 4), ('5', 8), ('8', 14), ('6', 1), ('2', 3),
                  ('1', 7), ('7', 9), ('9', 29), ('11', -1), ('13', -2), ('12', -8)]
        self.assertEqual(sorted_list, result)


if __name__ == '__main__':
    unittest.main()
