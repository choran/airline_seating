import os
import pandas as pd
refused = 0
remaining = 0
seperated = 0

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

    def allocate_row(csvFile):
      df = pd.read_csv("bookings.csv", sep=",", names=["Party","Number"])

      for index, row in df.iterrows():
        carryover = 0
        partyName = row['Party']
        partyNum = row['Number']
        print('Find %d seats for %s' %(partyNum,partyName))

        if(partyNum > remaining):
          refused += partyNum
        else:
          first_seat = check_seat(partyNum)

    def allocate_seats(number,seat):
      for i in range(number):
        check_set_ref(seat-i+1)
