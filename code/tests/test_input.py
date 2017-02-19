from unittest.mock import MagicMock, Mock, patch
import unittest
import sqlite3
<<<<<<< HEAD
import sys
sys.path.append('..')
from seat_assign_16200385_16201212_03783821 import Seating


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
        seating.seat_availability = {1: 4, 5: 1, 7: 2, 9: 1, 11: 1, 13: 4, 18: 3}
        group_num = 4
        exp_result = (1, 0)
        avail_seats = seating._sort_dict(group_num)
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
        seating.seat_availability = {1: 1, 3: 2, 5: 1, 7: 2, 9: 4, 13: 4, 18: 3}
        group_num = 3
        exp_result = (18, 0)
        avail_seats = seating._sort_dict(group_num)
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
        seating.seat_availability = {1: 1, 3: 2, 5: 1, 7: 2, 9: 2, 11: 1, 13: 3, 18: 3}
        group_num = 4
        exp_result = (18, -1)
        avail_seats = seating._sort_dict(group_num)
        self.assertEqual(avail_seats, exp_result)

    @patch('sqlite3.connect')
    def test_failed_connection(self, mock_connect):
        """
        Simple unittest for failed sqlite db connection
        """
        seating = Seating()
        sqlite3.connect = MagicMock(return_value='connection failed')
        seating.create_connection()
        sqlite3.connect.assert_called_with('')
        self.assertEqual(seating.connection, 'connection failed')

    def test_successful_connection(self):
        """
        Simple unittest for successful sqlite db connection
        """
        seating = Seating()
        seating.db_file = '":memory:"'
        seating.create_connection()
        self.assertIsInstance(seating.connection, sqlite3.Connection)
     
    def test_check_seat_ref(self):
        """
        Quick test of seat reference converter
        """
        seating = Seating()
        seating.seats_per_row = 6
        seating.num_to_let_mapping = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F',}
        seat = seating.check_seat_ref(8)
        exp_seat = (2,"B")
        self.assertEqual(seat, exp_seat)


if __name__ == '__main__':
    unittest.main()
