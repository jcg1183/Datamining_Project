import pandas as pd

from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
from sklearn.cluster import DBSCAN

# ***************************************************************
# Function:         sklearn_kmeans
# Variables/input:  objects.dataset
#                   int: k number of clusters to find
#                   int: number of datapoints to use
# Output:           pandas dataframe: cluster assignments
# Usage/Purpose:    Function uses sklearn's k-means algorithm
#                   to find clusters and return assignments.
# ***************************************************************
def sklearn_kmeans(ds, numClusters, numSamples):

    km = KMeans(
        n_clusters=numClusters,
        init="random",
        n_init=10,
        max_iter=300,
        tol=1e-04,
        random_state=0,
    )

    df = ds.df[["x1", "x2"]]
    df = df[:numSamples]

    km.fit(df[["x1", "x2"]].to_numpy())

    return pd.DataFrame(km.labels_, columns=["cluster"])


# ***************************************************************
# Function:         sklearn_kmedoids
# Variables/input:  objects.dataset
#                   int: k number of clusters to find
#                   int: number of datapoints to use
# Output:           pandas dataframe: cluster assignments
# Usage/Purpose:    Function uses sklearn's k-medoids algorithm
#                   to find clusters and return assignments.
# ***************************************************************
def sklearn_kmedoids(ds, numClusters, numSamples):

    km = KMedoids(n_clusters=numClusters, random_state=0)

    df = ds.df[["x1", "x2"]]
    df = df[:numSamples]

    km.fit(df[["x1", "x2"]].to_numpy())

    return pd.DataFrame(km.labels_, columns=["cluster"])


# ***************************************************************
# Function:         sklearn_dbscan
# Variables/input:  objects.dataset
#                   int: number of datapoints to use
#                   float: epsilon, radius of the neighborhood
#                   int: minimum points to form core object
# Output:           pandas dataframe: cluster assignments
# Usage/Purpose:    Function uses sklearn's dbscan algorithm
#                   to find clusters and return assignments.
# ***************************************************************
def sklearn_dbscan(ds, numSamples, epsilon, minPts):
    db = DBSCAN(eps=epsilon, min_samples=minPts)

    df = ds.df[["x1", "x2"]]
    df = df[:numSamples]

    db.fit(df[["x1", "x2"]].to_numpy())

    return pd.DataFrame(db.labels_, columns=["cluster"])