import settings

import numpy as np

# ***************************************************************
# Function:         calculate_sklearn_accuracy
# Variables/input:  pandas dataframe: list of experiment parameters
#                       and results
#                   objects.expriment
# Output:           writes accuracy to resultsDF
# Usage/Purpose:    Function calculates the accuracy of our
#                   algorithms' cluster assignments compared to
#                   the cluster assignments from the equivalent
#                   sklearn clustering algorithm.
# ***************************************************************
def calculate_sklearn_accuracy(resultsDF, exp):
    # add space to write accuracy for each experiment
    resultsDF["sklearn_accuracy"] = -1

    # loop through each experiment
    for i in range(resultsDF.shape[0]):
        # get the name of the algorithm used
        algo = resultsDF.iloc[i]["algo"]

        # skip algorithms not written by us
        if algo not in settings.algorithm_pairs.keys():
            continue

        # get parameters of this experiment
        datasetType = resultsDF.iloc[i]["dataset_type"]
        numPts = resultsDF.iloc[i]["num_pts"]
        trialNum = resultsDF.iloc[i]["trial_num"]
        epsilon = resultsDF.iloc[i]["epsilon"]
        minPts = resultsDF.iloc[i]["min_pts"]
        k = resultsDF.iloc[i]["k"]

        # find sklearn experiment results that matches this
        # experiment
        skRowIndex = resultsDF.index[
            (resultsDF["algo"] == settings.algorithm_pairs[algo])
            & (resultsDF["dataset_type"] == datasetType)
            & (resultsDF["num_pts"] == numPts)
            & (resultsDF["trial_num"] == trialNum)
            & (resultsDF["epsilon"] == epsilon)
            & (resultsDF["min_pts"] == minPts)
            & (resultsDF["k"] == k)
        ]

        # get the sklearn experiment row
        skRow = resultsDF.iloc[skRowIndex[0]]

        # write the accuracy result to the experiment
        resultsDF.loc[
            resultsDF.index.values == i, "sklearn_accuracy"
        ] = calculate_accuracy(
            numPts=resultsDF.iloc[i]["num_pts"],
            sk=skRow["cluster_list"],
            cl=resultsDF.iloc[i]["cluster_list"],
        )


# ***************************************************************
# Function:         calculate_groundtruth_accuracy
# Variables/input:  pandas dataframe: list of experiment parameters
#                       and results
#                   objects.expriment
# Output:           writes accuracy to resultsDF
# Usage/Purpose:    Function calculates the accuracy of our
#                   algorithms' cluster assignments compared to
#                   the cluster assignments from the sklearn
#                   dataset generator.
# ***************************************************************
def calculate_groundtruth_accuracy(resultsDF, exp):
    resultsDF["accuracy"] = -1

    for i in range(resultsDF.shape[0]):
        resultsDF.loc[resultsDF.index.values == i, "accuracy"] = calculate_accuracy(
            numPts=resultsDF.iloc[i]["num_pts"],
            ds=resultsDF.iloc[i]["dataset"],
            cl=resultsDF.iloc[i]["cluster_list"],
        )


# ***************************************************************
# Function:         calculate_accuracy
# Variables/input:  int: number of datapoints in dataset
#                   objects.dataset: dataset
#                   numpy.array: cluster assignments from sklearn
#                       algorithm
#                   numpy.array: cluster assignments from our
#                       algorithm
# Output:           writes accuracy to resultsDF
# Usage/Purpose:    Function calculates the set mappring from
#                   our clusters to sklearn generated clusters.
#                   Function creates an accuracy matrix between
#                   our cluster sets and sklearn cluster sets.
#                   Function then chooses most accurate mapping
#                   and returns an accuracy percentage.
# ***************************************************************
def calculate_accuracy(numPts=0, ds=None, sk=None, cl=None):
    gtClusters = 0
    ourClusters = 0

    # print("ds: {0}\nsk: {1}\ncl: {2}".format(type(ds), type(sk), type(cl)))

    # if parameter is type 'dataset' object
    if ds is not None:
        gtClusters = ds.df["y"]
        gtClusters = gtClusters[:numPts].values

    # if parameter is type numpy array
    elif sk is not None:
        gtClusters = sk["cluster"].tolist()

    # get our cluster assignments
    ourClusters = cl["cluster"].tolist()

    # dictionaries of clusters
    #   key: cluster number
    #   value: set(indexes of points in cluster)
    gtSetDict = {}
    ourSetDict = {}

    # build dictionary of sets
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

    # accuracy matrix to compare sets
    setMatrix = np.zeros([len(gtSetDict.keys()), len(ourSetDict.keys())])

    # mapping from dictionary key to array
    # index starting with 0
    imap = list(gtSetDict.keys())
    jmap = list(ourSetDict.keys())

    # calculate all accuracies
    for i in range(setMatrix.shape[0]):
        for j in range(setMatrix.shape[1]):

            gtSet = gtSetDict[imap[i]]
            ourSet = ourSetDict[jmap[j]]

            setMatrix[i][j] = float(len(gtSet & ourSet)) / len(gtSet)

    # dictionary holds mapping between out clusters
    # and sklearn clusters
    clusterMap = {}

    # loop through each sklearn cluster
    for i in range(setMatrix.shape[0]):
        jBest = setMatrix[i][0]
        jIndex = 0

        # loop through each of our clusters
        for j in range(setMatrix.shape[1]):
            if setMatrix[i][j] > jBest:
                jBest = setMatrix[i][j]
                jIndex = j

        # assign our most accurate cluster
        # to the sklearn cluster
        clusterMap[i] = jmap[jIndex]

    accuracy = 0
    totalRight = 0

    # get total points in correct cluster
    for i in range(setMatrix.shape[0]):
        gtSet = gtSetDict[imap[i]]
        ourSet = ourSetDict[clusterMap[i]]

        totalRight += len(gtSet & ourSet)

    # calculate accuracy of our algorithm
    # compared to sklearn algorithm
    accuracy = float(totalRight) / numPts

    return accuracy