import os
import pandas as pd
import sqlite3
import argparse

# Need to get value for dict
VALUE = 1

class Seating:
    def __init__(self):
        # Empty for now, may read input from text file or other source
        self.seat_availability = {}
        self.num_to_let_mapping = {}
        self.let_to_num_mapping = {}
        self.num_rows = 0
        self.seats_per_row = 0
        self.total_seats = 0

    def _evens1st(self, seats):
        num = seats[VALUE]
        # Test with modulus (%) two
        if num == 0:
            return 8000
        if num < 0:
            return num*(100)
        # It's an even number, return the value
        elif num % 2 == 0:
            return (num**-1)
        # It's odd, return the negated inverse
        else:
            return -1 * (num)

    def sort_dict(self, seats, group):
        """
        seats: dict of seat num as key and empty adjacent seats as value
        group: number of people in booking group
        :return: avail_seats - dict with seat num and seat num differentiator
        """

        avail_seats = {}
        for key, val in seats.items():
            # Need to calculated difference in available seats
            # and number in group
            avail_seats[key] = (val - group)

        # Now sort the avail seat dict so
        # 1: even numbers are first in asc order
        # 2: odd numbers are next in asc order
        # 3: negative numbers are next in desc order
        seat_diff = sorted(avail_seats.items(), key=self._evens1st, reverse=True)
        # Only interested in first element on sorted list
        # It is a tuple of set num and diff value
        return(seat_diff[0])

    def check_seat():
     print("")
    
    def check_booking(name,number):
        partyName = name
        partyNum = number    
        carryover = 0
        seat = check_seat(partyNum)
        while seat <0:
            carryover +=1
            partyNum -= 1
            seat = check_seat(partyNum)
    
        allocate_seats(partyName,partyNum,seat)
        
        if(carryover>0):
            check_booking(carryover)

    def allocate_bookings(csvFile):
        df = pd.read_csv("bookings.csv", sep=",", names=["Party","Number"])

        for index, row in df.iterrows():
            partyName = row['Party']
            partyNum = row['Number']
            print('Find %d seats for %s' %(partyNum,partyName))

        if(partyNum > remaining):
            refused += partyNum
        else:
            check_booking(partyName,partyNum)

    def allocate_seats(partyName,partyNum,seat):
        for i in range(partyNum):
            check_seat_ref(seat-i+1)
    
    def update_seat_file(self):
        print("")

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('db', type=str)
        parser.add_argument('csv', type=str)
        return parser.parse_args()

    def create_connection(self, db_file):
        '''

        :param db_file: filename of the SQLite database
        '''
        connection = sqlite3.connect(db_file)
        #TODO: Need to check for invalid connection at this point i.e. no DB file in location
        return connection

    def setup_plane_config(self, conn):
        '''

        :param connection:  connection to the SQLite DB
        :return:
        '''
        cursor = conn.cursor()
        cursor.execute("select nrows, seats from rows_cols")
        row = cursor.fetchone()

        self.num_rows = row[0]
        seat_layout = row[1]

        for key, char in enumerate(list(seat_layout)):
            self.num_to_let_mapping[key + 1] = char
            self.let_to_num_mapping[char] = key + 1

        self.seats_per_row = len(self.num_to_let_mapping)
        self.total_seats = self.num_rows * self.seats_per_row

        cursor.execute("select row, seat from seating where name <> '' order by row, seat")

        current_pointer = 1
        current_row = 1
        current_seat = 1
        count_consecutive = 0
        row_populated = False
        rec = cursor.fetchone()
        while rec is not None:
            new_row = rec[0]
            new_seat = self.let_to_num_mapping[rec[1]]
            print('new_row ' + str(new_row))
            print('new_seat ' + str(new_seat))

            if current_row != new_row:
                if(row_populated == False):
                    print('Row ' + str(current_row) + ' not populated!')
                    self.seat_availability[(current_row - 1) * self.seats_per_row + 1] = 0
                row_populated == False
                #print('Current Row != New Row')
                rest_of_row = (self.seats_per_row - current_seat) + 1
                self.seat_availability[current_pointer] = rest_of_row
                row_populated = True
                for i in range(current_row + 1, new_row):
                    current_pointer = ((i - 1) * self.seats_per_row) + 1
                    self.seat_availability[current_pointer] = self.seats_per_row
                    row_populated = True
                current_row = new_row
                current_seat = 1
                row_populated = False
                current_pointer = ((new_row - 1) * self.seats_per_row) + 1
                # process end of current row
                # process all interim rows

            #print('Current Row = New Row')
            if current_seat == new_seat:
                #print('Current Seat = New Seat')
                count_consecutive += 1
                current_seat += 1
                current_pointer = (current_row - 1) * self.seats_per_row + (new_seat + 1)
                #print('current_pointer ' + str(current_pointer))
            else:
                #print('Current Seat != New Seat')
                self.seat_availability[current_pointer] = new_seat - current_seat
                row_populated = True
                if new_seat == self.seats_per_row:
                    current_seat = 1
                    row_populated = False
                    current_row += 1
                    current_pointer = (current_row - 1) * self.seats_per_row + 1
                else:
                    current_seat = new_seat + 1
                    current_pointer = (current_row - 1) * self.seats_per_row + (new_seat + 1)
                count_consecutive = 1


            print('-----')
            print(self.seat_availability)
            print('-----')

            rec = cursor.fetchone()
            if rec is None:
                    if current_pointer <= self.total_seats: #will indicate that the last seat on the plane was already processed
                        new_row = self.num_rows + 1
                        rest_of_row = (self.seats_per_row - current_seat) + 1
                        self.seat_availability[current_pointer] = rest_of_row
                        for i in range(current_row + 1, new_row):
                            current_pointer = ((i - 1) * self.seats_per_row) + 1
                            self.seat_availability[current_pointer] = self.seats_per_row

        if not bool(self.seat_availability):
            for i in range (1, self.num_rows + 1):
                current_pointer = ((i - 1) * self.seats_per_row) + 1
                self.seat_availability[current_pointer] = self.seats_per_row

        print('-----')
        for (k, v) in sorted(self.seat_availability.items()):
            print('Key: ' + str(k) + ' Value: ' + str(v))
        print('-----')

refused = 0
remaining = 0
seperated = 0

#seating = Seating()

#args = seating.parse_args()
#print(args)
#connection = seating.create_connection(args.db)
#seating.setup_plane_config(connection)

