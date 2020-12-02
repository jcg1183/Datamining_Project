import settings

import numpy as np


def calculate_sklearn_accuracy(resultsDF, exp):
    resultsDF["sklearn_accuracy"] = -1

    for i in range(resultsDF.shape[0]):
        algo = resultsDF.iloc[i]["algo"]

        if algo not in settings.algorithm_pairs.keys():
            continue

        datasetType = resultsDF.iloc[i]["dataset_type"]
        numPts = resultsDF.iloc[i]["num_pts"]
        trialNum = resultsDF.iloc[i]["trial_num"]
        epsilon = resultsDF.iloc[i]["epsilon"]
        minPts = resultsDF.iloc[i]["min_pts"]
        k = resultsDF.iloc[i]["k"]

        skRowIndex = resultsDF.index[
            (resultsDF["algo"] == settings.algorithm_pairs[algo])
            & (resultsDF["dataset_type"] == datasetType)
            & (resultsDF["num_pts"] == numPts)
            & (resultsDF["trial_num"] == trialNum)
            & (resultsDF["epsilon"] == epsilon)
            & (resultsDF["min_pts"] == minPts)
            & (resultsDF["k"] == k)
        ]

        skRow = resultsDF.iloc[skRowIndex[0]]

        resultsDF.loc[
            resultsDF.index.values == i, "sklearn_accuracy"
        ] = calculate_accuracy(
            numPts=resultsDF.iloc[i]["num_pts"],
            sk=skRow["cluster_list"],
            cl=resultsDF.iloc[i]["cluster_list"],
        )


def calculate_groundtruth_accuracy(resultsDF, exp):
    resultsDF["accuracy"] = -1

    for i in range(resultsDF.shape[0]):
        resultsDF.loc[resultsDF.index.values == i, "accuracy"] = calculate_accuracy(
            numPts=resultsDF.iloc[i]["num_pts"],
            ds=resultsDF.iloc[i]["dataset"],
            cl=resultsDF.iloc[i]["cluster_list"],
        )


def calculate_accuracy(numPts=0, ds=None, sk=None, cl=None):
    gtClusters = 0
    ourClusters = 0

    # print("ds: {0}\nsk: {1}\ncl: {2}".format(type(ds), type(sk), type(cl)))

    # if parameters is type 'dataset' object
    if ds is not None:
        gtClusters = ds.df["y"]
        gtClusters = gtClusters[:numPts].values

    elif sk is not None:
        gtClusters = sk["cluster"].tolist()

    ourClusters = cl["cluster"].tolist()

    # print(type(ourClusters))
    # print(type(gtClusters))

    gtSetDict = {}
    ourSetDict = {}

    for i in range(len(gtClusters)):
        clust = gtClusters[i]

        if clust in gtSetDict.keys():
            gtSetDict[clust].add(i)
        else:
            gtSetDict[clust] = set([i])

    for i in range(len(ourClusters)):
        clust = ourClusters[i]

        if clust in ourSetDict.keys():
            ourSetDict[clust].add(i)
        else:
            ourSetDict[clust] = set([i])

    setMatrix = np.zeros([len(gtSetDict.keys()), len(ourSetDict.keys())])

    imap = list(gtSetDict.keys())
    jmap = list(ourSetDict.keys())

    for i in range(setMatrix.shape[0]):
        for j in range(setMatrix.shape[1]):

            gtSet = gtSetDict[imap[i]]
            ourSet = ourSetDict[jmap[j]]

            setMatrix[i][j] = float(len(gtSet & ourSet)) / len(gtSet)

    clusterMap = {}

    for i in range(setMatrix.shape[0]):
        jBest = setMatrix[i][0]
        jIndex = 0

        for j in range(setMatrix.shape[1]):
            if setMatrix[i][j] > jBest:
                jBest = setMatrix[i][j]
                jIndex = j

        clusterMap[i] = jmap[jIndex]

    accuracy = 0
    totalRight = 0

    for i in range(setMatrix.shape[0]):
        gtSet = gtSetDict[imap[i]]
        ourSet = ourSetDict[clusterMap[i]]

        totalRight += len(gtSet & ourSet)

    accuracy = float(totalRight) / numPts

    return accuracy