# variable and parameters for experiment and clustering algorithms

algorithms = [
    "DBSCAN",
    "sklearn_dbscan",
    "sklearn_kmeans",
    "sklearn_kmedoids",
    "k-means",
    "k-medoids",
]

algorithm_pairs = {
    "DBSCAN": "sklearn_dbscan",
    "k-means": "sklearn_kmeans",
    "k-medoids": "sklearn_kmedoids",
}

datasetTypes = ["circles", "moons", "blobs"]  # , "random"]

maxSamples = 100  # 2500
numSamples = [100]  # [500, 1000, 1500, 2000, 2500]

numRuns = 1

# Parameters for DBSCAN
epsilons = [0.1]  # [0.25, 0.4, 0.5]
minPts = [5]  # [15, 30, 45]

k = [2, 3, 4, 5]

description = {
    "k-means": "This is the description for k-means",
    "k-mediods": "This is the description for k-medoids",
    "DBSCAN": "This is the description for DBSCAN",
}
