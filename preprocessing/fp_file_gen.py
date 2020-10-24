import pandas as pd


# Using readlines()
file1 = open("input.txt", "r")
Lines = file1.readlines()

num_unique = int(Lines[0])
num_transactions = int(Lines[1])

items = []

# Strips the newline character
for line in Lines[2:]:
    list1 = line.split()
    items.append(list1[1:])

dict1 = {"items": items}

df = pd.DataFrame(dict1, columns=["items"])


unique_items = df.items.unique

print(len(unique_items))
print(unique_items)