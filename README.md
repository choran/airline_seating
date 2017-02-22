# airline_seating
MIS40750: Analytics Research &amp; Implementation

| Contributors     | Student ID |
|------------------|------------|
| Cathal Horan     | 03783821   |
| Cian Mc Leod     | 16200385   |
| Stephen O'Reilly | 16201212   |

## Assumptions
* The initial plane configuration can be given with any number of passengers seated in any area of the plane.
* A party of passengers are considered separated unless they can all sit on the same row with no passengers from other parties between them.
* Parties tend to travel in even groups with the most likely party consisting of two. 

If there are enough remaining seats on the plane, we will accommodate the passengers even if they need to be split up. Based on the above assumptions, seats are allocated in the following priority:  
1. An area of the plane which contains exactly the number of seats for the party.  
2. An area such that it will leave the smallest **even** remainder of seats after allocating the passengers those seats.  
3. An area such that it will leave the smallest **odd** remainder of seats after allocating the passengers those seats.  

If a party can't be accommodated together using the rules above, we try to accommodate the party minus one passenger until each member has been allocated a seat.

## Method
1. The seating configuration is parsed to give the number of seats per row and how the plane is structured.  
2. A dictionary of available seats is created taking into account the passengers already seated on the plane. They key of the dictionary is the seat number while the value is the available seats to the right of that seat (including the seat itself). On a traditional 3 by 3 plane, 5 refers to seat 1E while 8 refers to 2B.
3. Each booking in the CSV file is looped through. If there are enough seats to accommodate the booking, it is allocated according to the aforementioned rules. To do this, the dictionary is sorted by the value minus the party number and is sorted first by zeroes then evens then finally odds. The optimal seat is the first row of this sorted dictionary.
4. A seat reference is parsed from the dictionary entry and the database is updated.
5. If passengers must be separated, the booking is looped through until each party member has been given a seat. We try to allocate seats alongside the greatest number of passengers possible. For example, a party of five will be broken into 4 and 1 rather than 3 and 2 if possible.
6. Finally, the overall statistics of passengers refused and separated are updated in the database.

## Test Databases
We have included a number of test databases, which we used to test the program. They are all under code/tests:
1. airline_seating.db - The original sample database file
2. airline_seating_consecutive.db - A ten row, ABCDEF seat configuration plane with mainly consecutive passengers already seated
3. airline_seating_empty_plane.db - A fifteen row, ACDF seat configuration plane with no existing passengers
4. airline_seating_empty_rows.db - A nine row, ACDF seat configuration plane with multiple empty rows (and empty passengers!)
5. airline_seating_empty_seats.db - A fifteen row, ACDF seat configuration plane with all seats vacant, apart from the first two
6. airline_seating_full_plane.db - A fifteen row, ACDF seat configuration plane with all existing passengers

## GitHub Repository URL
https://github.com/choran/airline_seating

## Statement of Work
We began this assignment with a day long kick-off meeting, where we broke down the requirements from the specification, came up with a draft solution that we thought would satisfy the requirements given and then worked our way though test-case scenarios to ensure that our solution would be a viable one.
At the end of this meeting, we roughly broke up the tasks into three equal segments, those being 1) Database input / output and intial dictionary population, 2) The dictionary sorting algorithm which identifies the best row and 3) The booking allocation functionality which utilises the aforementioned dictionary to assign and store the seating details.
We then each took one of these sections and worked on them individually, before amalgamating our work into a single functioning class, complete with test cases and documentation.
