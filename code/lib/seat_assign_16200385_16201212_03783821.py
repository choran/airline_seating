import os


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

