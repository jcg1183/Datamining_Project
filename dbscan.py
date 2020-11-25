from sklearn import datasets

import numpy as np
import pandas as pd
import math
import itertools
import time


def dbscan(ds, numSamples, epsilon, minPts):
    df = ds.df.copy()

    clusterCount = 0

    df["neighbors"] = [[] for _ in range(df.shape()[0])]
    df["visited"] = 0
    df["cluster"] = -1

    distanceArray = get_distances(df)

    count_neighbors(df, distanceArray, epsilon)

    print("Running DBSCAN")

    dbscanTimeStart = time.perf_counter()

    while 0 in df["visited"].values:
        index = df[df.visited == 0].first_valid_index()

        # mark datapoint as visited
        df.at[index, "visited"] = 1

        # check if this datapoint has enough neighbors
        if len(df.iloc[index]["neighbors"]) < minPts:
            continue

        # add datapoint to a new cluster
        df.at[index, "cluster"] = clusterCount
        print(df.iloc[index]["cluster"])
        # queue of neighbors to check
        queue = []

        # add current datapoint's neighbors to queue
        for item in df.iloc[index]["neighbors"]:
            if df.iloc[item]["visited"] == 0:
                queue.append(item)

        while len(queue) > 0:
            index = queue.pop(0)

            if df.iloc[index]["visited"] == 1:
                continue

            df.at[index, "visited"] = 1

            if len(df.iloc[index]["neighbors"]) >= minPts:
                for item in df.iloc[index]["neighbors"]:
                    if df.iloc[item]["visited"] == 0:
                        queue.append(item)

            df.at[index, "cluster"] = clusterCount

        clusterCount += 1

    print("Finished")

    dbscanTimeStop = time.perf_counter()

    print("dbscan time: {0:5.4}\n".format((dbscanTimeStop - dbscanTimeStart) * 100))


def get_distances(df):
    print("get_distances")

    getDistancesTimeStart = time.perf_counter()

    numPoints = df.shape[0]

    distanceArray = np.zeros([numPoints, numPoints], dtype=float)

    for i in range(numPoints):
        for j in range(i, numPoints):
            if i == j:
                continue

            distance = math.sqrt(
                math.pow(df.iloc[i]["x1"] - df.iloc[j]["x1"], 2)
                + math.pow(df.iloc[i]["x2"] - df.iloc[j]["x2"], 2)
            )

            distanceArray[i, j] = distance
            distanceArray[j, i] = distance

    getDistancesTimeStop = time.perf_counter()

    print(
        "get_distances time: {0:5.4}\n".format(
            (getDistancesTimeStop - getDistancesTimeStart) * 100
        )
    )

    return distanceArray


def count_neighbors(df, distanceArray, epsilon):
    print("count_neighbors")

    countNeighborsTimeStart = time.perf_counter()

    for i in range(df.shape[0]):
        row = distanceArray[i, :]

        nestedList = np.argwhere(row < epsilon).tolist()

        flatList = list(itertools.chain.from_iterable(nestedList))

        df.iloc[i]["neighbors"].extend(flatList)

    countNeighborsTimeStop = time.perf_counter()

    print(
        "count_neighbors time: {0:5.4}\n".format(
            (countNeighborsTimeStop - countNeighborsTimeStart) * 100
        )
    )
