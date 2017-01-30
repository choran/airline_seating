import os
import pandas as pd
import sqlite3
import argparse

class Seating:
    def __init__(self):
        # Empty for now, may read input from text file or other source
        pass

    def evens1st(num):
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
    
    def update_seat_file:
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
        return connection

    def setup_plane_config(self, conn):
        '''

        :param connection:  connection to the SQLite DB
        :return:
        '''
        print(conn)
        cursor = conn.cursor()
        cursor.execute("select nrows, seats from rows_cols")
        row = cursor.fetchone()

        num_rows = row[0]
        seat_layout = row[1]

        num_to_let_mapping = {}
        let_to_num_mapping = {}
        for key, char in enumerate(list(seat_layout)):
            num_to_let_mapping[key + 1] = char
            let_to_num_mapping[char] = key + 1

        seats_per_row = len(num_to_let_mapping)
        total_seats = num_rows * seats_per_row
        print(num_to_let_mapping)
        print("Total Seats: " + str(total_seats))

        cursor.execute("select row, seat, name from seating where name <> '' order by row, seat")
        seat_availability = {}
        row = cursor.fetchone()
        for i in range(1, num_rows + 1):
            print("Row No,: " + str(i))
            if row[0] == i:
                print(num_to_let_mapping[1])
                print(row[1])
                seat_num = let_to_num_mapping[row[1]]
                print(seat_num)
                print(seat_availability)

            else:
                pointer = ((i - 1) * seats_per_row) + 1
                seat_availability[pointer] = seats_per_row
                print(seat_availability)


refused = 0
remaining = 0
seperated = 0

seating = Seating()

args = seating.parse_args()
print(args)
connection = seating.create_connection(args.db)
seating.setup_plane_config(connection)

