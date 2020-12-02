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

maxSamples = 2500
numSamples = [500, 1000, 1500, 2000, 2500]

numRuns = 1

# Parameters for DBSCAN
epsilons = [0.25, 0.4, 0.5]
minPts = [15, 30, 45]

description = {
    "k-means": "This is the description for k-means",
    "k-mediods": "This is the description for k-medoids",
    "DBSCAN": "This is the description for DBSCAN",
}
