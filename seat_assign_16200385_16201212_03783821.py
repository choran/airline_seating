import pandas as pd
refused = 0
remaining = 0
seperated = 0

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


  
