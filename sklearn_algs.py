from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
from sklearn.cluster import DBSCAN

import pandas as pd


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


def sklearn_kmedoids(ds, numClusters, numSamples):

    km = KMedoids(n_clusters=numClusters, random_state=0)

    df = ds.df[["x1", "x2"]]
    df = df[:numSamples]

    km.fit(df[["x1", "x2"]].to_numpy())

    return pd.DataFrame(km.labels_, columns=["cluster"])


def sklearn_dbscan(ds, numSamples, epsilon, minPts):
    db = DBSCAN(eps=epsilon, min_samples=minPts)

    df = ds.df[["x1", "x2"]]
    df = df[:numSamples]

    db.fit(df[["x1", "x2"]].to_numpy())

    return pd.DataFrame(db.labels_, columns=["cluster"])