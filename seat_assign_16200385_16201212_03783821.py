import os
import pandas as pd
import sqlite3
import argparse
import math

# Need to get value for dict
VALUE = 1


class Seating:
    def __init__(self):

        self.connection = None
        self.db_file = ""
        self.csv_file = ""
        self.seat_availability = {}
        self.num_to_let_mapping = {}
        self.let_to_num_mapping = {}

        self.db_file = ""
        self.csv_file = ""

        self.num_rows = 0
        self.seats_per_row = 0
        self.total_seats = 0
        self.refused = 0
        self.remaining = 0
        self.separated = 0

    def _evens1st(self, seats):
        num = seats[VALUE]
        # Test with modulus (%) two
        if num == 0:
            return 8000
        if num < 0:
            return num * (100)
        # It's an even number, return the value
        elif num % 2 == 0:
            return (num ** -1)
        # It's odd, return the negated inverse
        else:
            return -1 * (num)

    def _sort_dict(self, group):
        """
        group: number of people in booking group
        :return: avail_seats - tuple with seat num and seat num differentiator
        """

        avail_seats = {}
        for key, val in self.seat_availability.items():
            # Need to calculated difference in available seats
            # and number in group
            avail_seats[key] = (val - group)

        # Now sort the avail seat dict so
        # 1: even numbers are first in asc order
        # 2: odd numbers are next in asc order
        # 3: negative numbers are next in desc order
        seat_diff = sorted(avail_seats.items(), key=self._evens1st, reverse=True)
        # Only interested in first element on sorted list
        # It is a tuple of seat num and diff value
        return seat_diff[0]

    def check_booking(self, name, number, push_carryover):
        """
        name: Name of party
        number: Number travelling
        push_carryover: Boolean of whether first call to function which will update separated passengers.
        """
        # Check best seating position by iterating until party is small enough to be allocated
        partyNum = number
        carryover = 0
        seat = self._sort_dict(number)
        while seat[1] < 0:
            carryover += 1
            partyNum -= 1
            seat = self._sort_dict(partyNum)

        # Decrease the remaining passengers the plane can take.
        self.remaining -= partyNum
        # Update dictionary of available seats and allocate seats in database
        self.seat_availability[seat[0]] -= partyNum
        self.allocate_seats(name, partyNum, seat)

        # If party had to be split up, update statistics and allocate seats for those separated.
        if carryover > 0:
            # On the first run through, we update the passengers separated.
            # On second run, these have already been accounted for.
            if push_carryover == True:
                self.separated += number
            # Iterate through again looking for seats for the separated passengers
            self.check_booking(name, carryover, False)

    def allocate_bookings(self):
        # Access the CSV through Pandas and store.
        df = pd.read_csv(self.csv_file, sep=",", names=["Party", "Number"])

        # iterate through each booking to allocate seats.
        for index, row in df.iterrows():
            partyName = row['Party']
            partyNum = row['Number']

            # If we can't accommodate them then refuse else allocate some seat.
            if partyNum > self.remaining:
                self.refused += partyNum
            else:
                self.check_booking(partyName, partyNum, True)

    def allocate_seats(self, partyName, partyNum, startSeat):
        """
        partyName: Name of party
        partyNum: Number travelling
        startSeat: Information on the starting seat which the party should be filled from.
        """
        # empty array to store allocated deats/
        seats = []
        # Find the seat references for each of the passengers
        for i in range(1, partyNum + 1):
            # The seat reference is starting position + leftover seats after allocation + party number - passenger number
            seat = self.check_seat_ref(startSeat[0] + startSeat[1] + partyNum - i)
            seats.append(seat)

        # Update the database with the seats each passenger has been allocated.
        cursor = self.connection.cursor()
        # (partyName, seats)
        for item in seats:
            cursor.execute("UPDATE seating SET name='%s' WHERE row=%d AND seat='%s';" % (partyName, item[0], item[1]))
        self.connection.commit()

    def check_seat_ref(self, seatNum):
        """
        seatNum: The numerical seat reference e.g. 6
        :return: Tuple with common seat refernce e.g. (1,F)
        """
        # Row number of the seat, rounded up to integer
        row = math.ceil(seatNum / self.seats_per_row)
        # The number mapping of the seat.
        seatMap = seatNum - (row - 1) * self.seats_per_row
        # Access the letter mapping the seat corresponds to.
        seatLetter = self.num_to_let_mapping[seatMap]
        # Return the seat in tuple
        seat_ref = (row, seatLetter)
        return seat_ref

    def parse_args(self):
        """
        Function will read in the database location and bookings location arguments
        and store them in the class for re-use
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('db', type=str)
        parser.add_argument('csv', type=str)
        args = parser.parse_args()

        self.db_file = args.db
        self.csv_file = args.csv

    def create_connection(self):
        '''
        Function will create the connection to the sqlite3 database using the provided command-line arguments
        '''
        self.connection = sqlite3.connect(self.db_file)

    def destroy_connection(self):
        '''
        Function will destroy the connection to the sqlite3 database
        '''
        self.connection.close()

    def get_plane_layout(self):
        '''
        Function will retrieve the plane layout parameters from the DB
        and then populate the related variables e.g. total_seats and let_to_num_mapping
        '''
        cursor = self.connection.cursor()
        cursor.execute("SELECT nrows, seats FROM rows_cols")
        row = cursor.fetchone()

        self.num_rows = row[0]  # Number of rows on the plane
        seat_layout = row[1]

        for key, char in enumerate(list(seat_layout)):
            self.num_to_let_mapping[key + 1] = char  # Mapping of seat numbers to their representative letters
            self.let_to_num_mapping[char] = key + 1  # Mapping of seat letters to their representative numbers

        self.seats_per_row = len(self.num_to_let_mapping)  # Number of seats per row on the plane
        self.total_seats = self.num_rows * self.seats_per_row  # Total number of seats on the plane
        self.remaining = self.total_seats  # Number of seats still available on the plane

    def populate_seat_availability(self):
        '''
        Function will traverse the seating data from the DB and generate a free seat mapping for the plane.
        For instance, if seats B, E and F are free on row 1, then the dict will contain {2: 1, 5: 2}
        '''

        # Retrieve all previously bought seats on the plane in row, seat order
        cursor = self.connection.cursor()
        cursor.execute("SELECT row, seat FROM seating WHERE name <> '' ORDER BY row, seat")

        # set initial variables for traversal
        current_pointer = 1
        current_row = 1
        current_seat = 1
        count_consecutive = 0
        row_populated = False
        rec = cursor.fetchone()

        # While there are more passengers...
        while rec is not None:
            self.remaining -= 1
            # Get the row and seat for the passenger
            new_row = rec[0]
            new_seat = self.let_to_num_mapping[rec[1]]

            # If the next passenger to be processed is not on the same row as the previous passenger
            if current_row != new_row:
                if row_populated == False:
                    # Create entry for fully empty row
                    self.seat_availability[(current_row - 1) * self.seats_per_row + 1] = 0
                row_populated = False

                # Create entry for the rest of the row
                rest_of_row = (self.seats_per_row - current_seat) + 1
                self.seat_availability[current_pointer] = rest_of_row
                row_populated = True

                # For each row between current and previous row, create entry for fully empty row
                for i in range(current_row + 1, new_row):
                    current_pointer = ((i - 1) * self.seats_per_row) + 1
                    self.seat_availability[current_pointer] = self.seats_per_row
                    row_populated = True

                # Set variables for next iteration
                current_row = new_row
                current_seat = 1
                row_populated = False
                current_pointer = ((new_row - 1) * self.seats_per_row) + 1

            # Process consecutive seats
            if current_seat == new_seat:
                # Add to counter and move the pointers on to the next seat
                count_consecutive += 1
                current_seat += 1
                current_pointer = (current_row - 1) * self.seats_per_row + (new_seat + 1)

            # Process next passenger on the same row i.e non-consecutive seats purchased
            else:
                # Find intervening seats and use this to populate the mapping
                self.seat_availability[current_pointer] = new_seat - current_seat
                row_populated = True

                # Handle end of aisle seats
                if new_seat == self.seats_per_row:
                    current_seat = 1
                    row_populated = False
                    current_row += 1
                    current_pointer = (current_row - 1) * self.seats_per_row + 1
                else:
                    current_seat = new_seat + 1
                    current_pointer = (current_row - 1) * self.seats_per_row + (new_seat + 1)

                count_consecutive = 1

            # Populate the rest of the plane once all occupied seats have been processed
            rec = cursor.fetchone()
            if rec is None:
                # Check that the last seat on the plane was already processed
                if current_pointer <= self.total_seats:

                    # Populate rest of current row
                    new_row = self.num_rows + 1
                    rest_of_row = (self.seats_per_row - current_seat) + 1
                    self.seat_availability[current_pointer] = rest_of_row

                    # For remaining rows, populate fully empty row
                    for i in range(current_row + 1, new_row):
                        current_pointer = ((i - 1) * self.seats_per_row) + 1
                        self.seat_availability[current_pointer] = self.seats_per_row

        # Handle empty passenger list scenario
        if not bool(self.seat_availability):
            for i in range(1, self.num_rows + 1):
                current_pointer = ((i - 1) * self.seats_per_row) + 1
                self.seat_availability[current_pointer] = self.seats_per_row

    def populate_statistics(self):
        '''
        Function will populate the DB with the plane statistics i.e. passengers_refused, passengers_separated
        '''
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE metrics SET passengers_refused = %d, passengers_separated = %d;" % (self.refused, self.separated))
        self.connection.commit()

    def print_statistics(self):
        print("Total number of seats: %d" % self.total_seats)
        print("Number of rows: %d" % self.num_rows)
        print("Number of seats per row: %d" % self.seats_per_row)
        print("Total number of seats remaining: %d" % self.remaining)
        print("Total number of seats separated: %d" % self.separated)
        print("Total number of seats refused: %d" % self.refused)


if __name__ == '__main__':
    seating = Seating()

    seating.parse_args()
    seating.create_connection()
    seating.get_plane_layout()
    seating.populate_seat_availability()
    seating.allocate_bookings()
    seating.populate_statistics()
    seating.destroy_connection()
    seating.print_statistics()