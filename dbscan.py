import math
import itertools
import time

import numpy as np
import pandas as pd
from sklearn import datasets


# ***************************************************************
# Function:         dbscan
# Variables/input:  objects.dataset
#                   int: number of datapoints
#                   float: epsilon, radius of neighborhood
#                   int: minimum number of points in neighborhood
# Output:           pandas dataframe: cluster assignment results
# Usage/Purpose:    Function performs classic dbscan by identifying
#                   core objects, clusters, and noise.
# ***************************************************************
def dbscan(ds, numSamples, epsilon, minPts):
    # prepare dataframe for function work
    df = ds.df.copy()
    df = df[:numSamples]
    clusterCount = 0

    # add functional columns to dataframe
    df["neighbors"] = [[] for _ in range(numSamples)]
    df["visited"] = 0
    df["cluster"] = -1

    # get a list of neighbors of each datapoint
    count_neighbors(df, ds.distanceArray[:numSamples, :numSamples], epsilon)

    # continue while there are unvisited datapoints
    while 0 in df["visited"].values:
        # get next datapoint that needs processing
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

        # continue while queue is not empty
        while len(queue) > 0:
            index = queue.pop(0)

            # skip if datapoint has been visited
            if df.iloc[index]["visited"] == 1:
                continue

            # mark datapoint as visited
            df.at[index, "visited"] = 1

            # add this points neighbors to queue if the
            # point meets the minimum points requirement
            if len(df.iloc[index]["neighbors"]) >= minPts:
                for item in df.iloc[index]["neighbors"]:
                    if df.iloc[item]["visited"] == 0:
                        queue.append(item)

            # assign a cluster number to datapoint
            df.at[index, "cluster"] = clusterCount

        # clusterCount assigns the cluster number to a datapoint
        clusterCount += 1

    return pd.DataFrame(df["cluster"], columns=["cluster"])


# ***************************************************************
# Function:         count_neighbors
# Variables/input:  pandas dataframe: dataset
#                   numpy 2d array: distance array
#                   float: epsilon, radius of neighborhood
# Output:           writes list of neighbors to dataframe
# Usage/Purpose:    Function finds a list of neighbors for each
#                   point based on epsilon value.
# ***************************************************************
def count_neighbors(df, distanceArray, epsilon):
    # loop through each datapoint
    for i in range(df.shape[0]):
        # pull out all distances from this point to all others
        row = distanceArray[i, :]

        # create a list of neighbors who are within epsilon
        nestedList = np.argwhere(row < epsilon).tolist()

        # flatten list
        flatList = list(itertools.chain.from_iterable(nestedList))

        # write list to datapoint["neighbors"]
        df.iloc[i]["neighbors"].extend(flatList)