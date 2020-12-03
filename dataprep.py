import math
import time

from objects import dataset
import settings

import numpy as np
import pandas as pd
from sklearn import datasets


# ***************************************************************
# Function:         ready_datasets
# Variables/input:  argparse.arguments object
# Output:           python list containing objests.dataset
# Usage/Purpose:    Function loads a dataset from a csv file
#                   or generates datasets using sklearn.dataset.
#                   CSV datasets are specified by command line
#                   argument and sklearn datasets are specified
#                   in settings.py.
# ***************************************************************
def ready_datasets(args):
    datasetReturn = []

    # load dataset from csv.  this has not been tested
    # the csv part could be abstracted into another function
    if args.dataset:
        dfCSV = pd.read_csv(args.dataset)
        datasetReturn.append(dataset(args.dataset[2:-4], dfCSV))

        settings.datasetTypes.insert(0, args.dataset[2:-4])

        print("dataset read from {0}".format(args.dataset[2:-4]))
        print(dfCSV.head(5))

    # loop through all sklearn dataset types and add a new
    # dataset object to the return list
    if args.generate:
        for name in settings.datasetTypes:
            datasetReturn.append(dataset(name, build_dataset(name)))

    return datasetReturn


# ***************************************************************
# Function:         build_dataset
# Variables/input:  string: name
# Output:           pandas dataframe
# Usage/Purpose:    Function builds and returns specified
#                   dataset.
# ***************************************************************
def build_dataset(name):
    # build all the dataset types here
    df = pd.DataFrame()

    # generate sklearn datasets
    if name == "circles":
        new_dataset = datasets.make_circles(
            n_samples=settings.maxSamples, factor=0.5, noise=0.05
        )

    elif name == "moons":
        new_dataset = datasets.make_moons(n_samples=settings.maxSamples, noise=0.05)

    elif name == "blobs":
        new_dataset = datasets.make_blobs(n_samples=settings.maxSamples, random_state=1)

    # random needs updating
    elif name == "random":
        # Fitting a pentagon in a square hole, needs updating asap
        random = np.random.uniform(low=0.0, high=15.0, size=(200, 2))
        df = pd.DataFrame(columns=["x1", "x2"])
        df.x1 = random[:, 0]
        df.x2 = random[:, 1]
        return df

    # convert to dataframe
    df = pd.DataFrame(new_dataset[0], columns=["x1", "x2"])

    # add cluster labels to dataframe
    df["y"] = new_dataset[1]

    return df


# ***************************************************************
# Function:         calculate_distances
# Variables/input:  objects.exp
# Output:           appends distance matrix to dataset
# Usage/Purpose:    Function takes a dataset and creates a
#                   distance matrix for that dataset.
# ***************************************************************
def calculate_distances(exp):
    print("calculate_distances")

    for ds in exp.datasets:
        df = ds.df

        getDistancesTimeStart = time.perf_counter()

        ds.distanceArray = np.zeros(
            [settings.maxSamples, settings.maxSamples], dtype=float
        )

        for i in range(settings.maxSamples):
            for j in range(i, settings.maxSamples):
                if i == j:
                    continue

                distance = math.sqrt(
                    math.pow(df.iloc[i]["x1"] - df.iloc[j]["x1"], 2)
                    + math.pow(df.iloc[i]["x2"] - df.iloc[j]["x2"], 2)
                )

                ds.distanceArray[i, j] = distance
                ds.distanceArray[j, i] = distance

        getDistancesTimeStop = time.perf_counter()

        print(
            "{0} get_distances time: {1:5.4}".format(
                ds.name, (getDistancesTimeStop - getDistancesTimeStart) * 100
            )
        )
