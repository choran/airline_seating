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
