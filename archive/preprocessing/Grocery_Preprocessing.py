# Grocery Preprocessing
# Takes the Groceries Dataset and combines all transactions that share
# a member number and date and adds transaction ids to all transactions.

import pandas as pd
import os
from subprocess import call

# Load dataset into a Dataframe
df = pd.read_csv("Groceries_dataset.csv")

# Sort the rows by their member numbers
df = df.sort_values(by="Member_number")

# Create new DataFrame for cleaned data
df_clean = pd.DataFrame(columns=df.columns)

# Get the number of unique items in the dataset
unique_items = len(pd.Series.unique(df['itemDescription']))

# Hardcoded Member_number range and loop
for Member_number in range(1000, 5001):
    
    # Console feedback statements
    if Member_number == 1000:
        print("Cleaning transactions for Members",Member_number,"to",Member_number+1000)
    elif Member_number == 5000:
        print("Complete!\n")
    elif Member_number % 1000 == 0:
        print("Cleaning transactions for Members",Member_number,"to",Member_number+1000)
    
    # Get all rows for the current member
    df_slice = df[df['Member_number'] == Member_number]
    df_temp = pd.DataFrame(columns = df.columns)
    
    for n in range(0, len(df_slice)):
        
        # Get the current transaction date
        date = df_slice.iloc[n]['Date']
        
        # If the current transaction date is already in the temporary DataFrame,
        # append the current transaction's item to the existing row
        if date in df_temp.Date.values:
            
            temp = df_temp[df_temp['Date'] == date].values[0]
            temp[2].append(df_slice.iloc[n]['itemDescription'])
        
        # Else, create a new row in the temporary DataFrame
        else:
            
            # Convert the new row's itemDescription into a list
            new_row = list(df_slice.iloc[n])
            new_row[2] = [new_row[2]]
            new_row = pd.DataFrame([new_row], columns=df.columns)
            
            # Append new row
            df_temp = df_temp.append(new_row, ignore_index=True)
    
    # Append the temporary DataFrame to the cleaned DataFrame
    df_clean = df_clean.append(df_temp, ignore_index=True)

# Sort the rows by their dates
df_clean = df_clean.sort_values(by="Date")

# Prepare Transaction_id list and padding
Transaction_id = []
pad = len(str(len(df_clean)))

# Create the Transaction_id column
for n in range(0, len(df_clean)):
    
    n = str(n)
    new_id = "T" + n.zfill(pad)
    Transaction_id.append(new_id)
    
# Add the Transaction_id column to the cleaned DataFrame
df_clean['Transaction_id'] = Transaction_id
# Get the number of transactions in the updated DataFrame
transaction_count = len(df_clean)

print("Unique Items:", unique_items)
print("Transaction count:", transaction_count)
print(df_clean)

# Export the updated dataset to csv
df_clean.to_csv('Updated_Groceries_dataset.csv')

# If an input file already exists, remove it
if os.path.exists("input.txt"):
    os.remove("input.txt")

# Create a new input file using the updated DataFrame
with open("input.txt","a") as f:
    
    # Append unique item count and transaction count
    print(unique_items, file=f)
    print(transaction_count, file=f)
    
    # For every row in the DataFrame
    for n in range(0, transaction_count):
        
        # Get the number of items
        num_items = len(df_clean.iloc[n]['itemDescription'])
        
        # Get a copy of the itemDescription list
        items = df_clean.iloc[n]['itemDescription'].copy()
        line = ""
        
        # Replace all spaces in the item names with underscores
        for i in range(0, len(items)):
            line += " " + items[i].replace(" ","_")
        
        # Append data to the input file
        print(num_items, line, file=f)
