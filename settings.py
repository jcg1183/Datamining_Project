algorithms = [
    "DBSCAN",
    "sklearn_kmeans",
    "sklearn_kmedoids",
    "sklearn_dbscan",
]  # , "k-means", "k-medoids"]

datasetTypes = ["circles", "moons", "blobs"]  # , "random"]

maxSamples = 100
numSamples = [100]  # , 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2500]

numRuns = 5

# Parameters for DBSCAN
epsilons = [0.5]  # , 0.1, 0.15]  # , 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
minPts = [10]  # , 10, 15]  # , 20, 25, 30, 35, 40, 45, 50]

description = {
    "k-means": "This is the description for k-means",
    "k-mediods": "This is the description for k-medoids",
    "DBSCAN": "This is the description for DBSCAN",
}
