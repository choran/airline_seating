import os
import pandas as pd
import sqlite3
import argparse

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
