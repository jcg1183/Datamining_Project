import pandas as pd
import settings
import random


dict1 = {}

dict1["x1"] = []
dict1["x2"] = []
dict1["y"] = []

for i in range(settings.maxSamples):
    dict1["x1"] = random.uniform(-1, 1)
    dict1["x2"].append(random.uniform(-1, 1))
    dict1["y"].append(random.randint(0, 2))

df = pd.DataFrame(dict1)

df.to_csv(r"test_dataset.csv", index=False)


print(df.head())
