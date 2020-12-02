import math
import time

from objects import dataset
import settings

import numpy as np
import pandas as pd
from sklearn import datasets


# add appropriate comments
# this function uses command line arguments to generate
# datasets from csv or sklearn
def ready_datasets(args):
    datasetReturn = []

    # load dataset from csv.  this has not been tested
    # the csv part could be abstracted into another function
    if args.dataset:
        dfCSV = pd.read_csv(args.dataset, columns=["x1", "x2"])
        datasetReturn.append(dataset(args.dataset, dfCSV))

        print("dataset read from {0}".format(args.dataset))
        print(dfCSV.head(5))

    # loop through all sklearn dataset types and add a new
    # dataset object to the return list
    if args.generate:
        for name in settings.datasetTypes:
            datasetReturn.append(dataset(name, build_dataset(name)))

    return datasetReturn


# add formatted comments
# function takes the name of an sklearn dataset type
# and builds a dataframe dataset of that type
def build_dataset(name):
    # build all the dataset types here
    df = pd.DataFrame()

    # generate sklearn circles dataset
    if name == "circles":
        new_dataset = datasets.make_circles(
            n_samples=settings.maxSamples, factor=0.5, noise=0.05
        )

    elif name == "moons":
        new_dataset = datasets.make_moons(n_samples=settings.maxSamples, noise=0.05)

    elif name == "blobs":
        new_dataset = datasets.make_blobs(n_samples=settings.maxSamples, random_state=1)

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
