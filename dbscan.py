from sklearn import datasets

import numpy as np
import pandas as pd
import math
import itertools
import time


def dbscan(ds, numSamples, epsilon, minPts):
    df = ds.df.copy()
    df = df[:numSamples]
    clusterCount = 0

    df["neighbors"] = [[] for _ in range(numSamples)]
    df["visited"] = 0
    df["cluster"] = -1

    count_neighbors(df, ds.distanceArray[:numSamples, :numSamples], epsilon)

    print(
        "Running DBSCAN:\n\tnumSamples: {0}\n\tepsilon: {1}\n\tminPts: {2}".format(
            numSamples, epsilon, minPts
        )
    )

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

    return df["cluster"]


def count_neighbors(df, distanceArray, epsilon):
    for i in range(df.shape[0]):
        row = distanceArray[i, :]

        nestedList = np.argwhere(row < epsilon).tolist()

        flatList = list(itertools.chain.from_iterable(nestedList))

        df.iloc[i]["neighbors"].extend(flatList)