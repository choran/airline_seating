import unittest
from lib.seat_assign import Seating


class TestInput(unittest.TestCase):
    def test_even_sort(self):
        """
        Simple test list just to have test in framework
        input =  [7, 3, 4, 8, 1, 9, 14, 29, 0, -1, -8, -2]
        """
        seating = Seating()
        input = {'1': 7, '2': 3, '4': 4, '5': 8, '6': 1, '7': 9, '8': 14,
                  '9': 29, '10': 0, '11': -1, '12': -8, '13': -2}
        sorted_list = sorted(input.items(), key=seating._evens1st, reverse=True)
        exp_result = [('10', 0), ('4', 4), ('5', 8), ('8', 14), ('6', 1), ('2', 3),
                  ('1', 7), ('7', 9), ('9', 29), ('11', -1), ('13', -2), ('12', -8)]
        self.assertEqual(sorted_list, exp_result)

    def test_sort_dict_4_toget_r1(self):
        """
        Verify that the sort_dict method returns valid tuple combo when
        there is adjacent number of seats available for booking group
        i.e. group is able to be seated together
        R|Seats
        1|_ _ _ _
        2|_ X _ _
        3|_ X _ X
        4|_ _ _ _
        5|X _ _ _
        For a new booking of 4 they should be seated in row 1
        """
        seating = Seating()
        seat_nums = {1: 4, 5: 1, 7: 2, 9: 1, 11: 1, 13: 4, 18: 3}
        group_num = 4
        exp_result = (1, 0)
        avail_seats = seating.sort_dict(seat_nums, group_num)
        self.assertEqual(avail_seats, exp_result)


    def test_sort_dict_3_toget_r4(self):
        """
        Verify that the sort_dict method returns valid tuple combo when
        there is adjacent number of seats available for booking group
        i.e. group is able to be seated together on line with 3 empty
        seats (row 5 in this case)
        R|Seats
        1|_ X _ _
        2|_ X _ _
        3|_ _ _ _
        4|_ _ _ _
        5|X _ _ _
        For a new booking of 4 they should be seated in row 4
        """
        seating = Seating()
        seat_nums = {1: 1, 3: 2, 5: 1, 7: 2, 9: 4, 13: 4, 18: 3}
        group_num = 3
        exp_result = (18, 0)
        avail_seats = seating.sort_dict(seat_nums, group_num)
        self.assertEqual(avail_seats, exp_result)

    def test_sort_dict_4_not_toget(self):
        """
        Verify that the sort_dict method returns valid tuple combo when
        there is adjacent number of seats available for booking group
        i.e. group is able to be seated together
        R|Seats
        1|_ X _ _
        2|_ X _ _
        3|_ _ X _
        4|_ _ _ X
        5|X _ _ _
        For a new booking of 4 we should return negative number since
        this indicates that there are no available adjacent seats
        """
        seating = Seating()
        seat_nums = {1: 1, 3: 2, 5: 1, 7: 2, 9: 2, 11: 1, 13: 3, 18: 3}
        group_num = 4
        exp_result = (18, -1)
        avail_seats = seating.sort_dict(seat_nums, group_num)
        self.assertEqual(avail_seats, exp_result)

if __name__ == '__main__':
    unittest.main()
