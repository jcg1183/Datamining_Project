#!/usr/bin/env python

import argparse
import math
import sys
import time

import settings
from objects import experiment, dataset
from dataprep import calculate_distances, build_dataset, ready_datasets
from dbscan import dbscan
from KBRAIN import run_kbrain, autoplot
from sklearn_algs import sklearn_kmeans, sklearn_kmedoids, sklearn_dbscan
from metrics import calculate_groundtruth_accuracy, calculate_sklearn_accuracy
from results_analysis import save_results, compile_results

import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.metrics import silhouette_score, pairwise_distances


# display all columns of a dataframe
pd.set_option("display.max_columns", None)
pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", None)


def main():
    # process command line arguments and return arguments as args
    args = run_parser()

    # load or build datasets according to arguments
    datasets = ready_datasets(args)

    # build experiment object, including datasets
    exp = experiment(datasets, settings.algorithms)

    # calculate distances for each dataset
    calculate_distances(exp)

    # run an experiment with all algorithms and datasets
    if args.experiment:
        run_experiment(exp)

    # run k-means algorithm on specified datasets
    if args.kmeans:
        # call k-means wrapper function
        print()

    if args.kmedoids:
        # call k-medoids wrapper function
        print()

    if args.dbscan:
        # call dbscan wrapper function
        print()

    # process results here
    # print_results(exp)

    # compile results into a dataframe
    resultsDF = compile_results(exp)

    # print(resultsDF.drop(columns=["cluster_list"]))

    calculate_groundtruth_accuracy(resultsDF, exp)

    calculate_sklearn_accuracy(resultsDF, exp)

    print(resultsDF.drop(columns=["cluster_list", "dataset"]))

    save_results(resultsDF)


# replace this comment with proper formater
# this function takes an experiment and runs
# all specified permutations of the parameters
def run_experiment(exp):
    # loop through each clustering algorithm
    for algo in exp.algorithms:

        # loop through each dataset
        for ds in exp.datasets:

            # loop through the number of datapoints
            # to be used
            for num in settings.numSamples:

                # loop for each trial run
                for i in range(1, settings.numRuns + 1):
                    print(
                        "algo: {0}, ds: {1}, size: {2}".format(algo, ds.name, num),
                        end="",
                    )
                    startTime = time.perf_counter()

                    # call dbscan with parameters
                    if algo == "DBSCAN":

                        # loop parameters unique to dbscan
                        for eps in settings.epsilons:
                            for mp in settings.minPts:

                                # call dbscan with parameters
                                results = dbscan(ds, num, eps, mp)
                                # save results of each experiment
                                exp.results[algo].append(
                                    (ds.name, num, i, eps, mp, results)
                                )

                    if algo == "k-means":

                        for k in range(3, 5):
                            clusters = run_kbrain(k, algo, ds)
                            exp.results[algo].append((ds.name, num, i, k, clusters))

                    if algo == "k-medoids":

                        for k in range(3, 5):
                            clusters = run_kbrain(k, algo, ds)
                            exp.results[algo].append((ds.name, num, i, k, clusters))

                    if algo == "sklearn_kmeans":
                        for numClusters in range(3, 5):
                            results = sklearn_kmeans(ds, numClusters, num)

                            exp.results[algo].append(
                                (ds.name, num, i, numClusters, results)
                            )

                    if algo == "sklearn_kmedoids":
                        for numClusters in range(3, 5):
                            results = sklearn_kmedoids(ds, numClusters, num)

                            exp.results[algo].append(
                                (ds.name, num, i, numClusters, results)
                            )

                    if algo == "sklearn_dbscan":
                        # loop parameters unique to dbscan
                        for eps in settings.epsilons:
                            for mp in settings.minPts:

                                # call dbscan with parameters
                                results = sklearn_dbscan(ds, num, eps, mp)

                                # save results of each experiment
                                exp.results[algo].append(
                                    (ds.name, num, i, eps, mp, results)
                                )

                    stopTime = time.perf_counter()

                    print(" {0:3.2} minutes".format((stopTime - startTime) / 60))


def print_results(exp):
    print("Analyse Results\n")

    for algo in exp.results.keys():
        if algo == "DBSCAN" or algo == "sklearn_dbscan":
            all_results = exp.results[algo]

            for results in all_results:
                print(
                    "Experiment:\n\tAlgorithm: {0}\n\tDataset Name: {1}\n\tNum Datapoints: {2}\n\tTrial Number: {3}\n\tEpsilon: {4}\n\tMin Points: {5}".format(
                        algo, results[0], results[1], results[2], results[3], results[4]
                    )
                )
                print("Cluster Assignments:\n")
                print(results[5])

        elif algo == "k-means" or algo == "sklearn_kmeans":
            all_results = exp.results[algo]

            for results in all_results:
                print(
                    "Experiment:\n\tAlgorithm: {0}\n\tDataset Name: {1}\n\tNum Datapoints: {2}\n\tTrial Number: {3}\n\tNumber Clusters: {4}".format(
                        algo, results[0], results[1], results[2], results[3]
                    )
                )
                print("Cluster Assignments:\n")
                print(results[4])

        elif algo == "k-medoids" or algo == "sklearn_kmedoids":
            all_results = exp.results[algo]

            for results in all_results:
                print(
                    "Experiment:\n\tAlgorithm: {0}\n\tDataset Name: {1}\n\tNum Datapoints: {2}\n\tTrial Number: {3}\n\tNumber Clusters: {4}".format(
                        algo, results[0], results[1], results[2], results[3]
                    )
                )
                print("Cluster Assignments:\n")
                print(results[4])


# add formatted comments
# this function uses 'argparse' library to parse
# command line arguments
# this function will terminate program if inappropriate
# arguments are given
# more checks of arguments need to be coded
def run_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d", "--dataset", action="store", help="path to a csv dataset {./dataset.csv}"
    )
    parser.add_argument(
        "-g", "--generate", action="store_true", help="generate all dataset types"
    )

    parser.add_argument(
        "-e", "--experiment", action="store_true", help="run all clustering algorithms"
    )

    parser.add_argument(
        "-m", "--kmeans", action="store_true", help="run only the k-means algorithm"
    )

    parser.add_argument(
        "-o", "--kmedoids", action="store_true", help="run only the k-medoids algorithm"
    )

    parser.add_argument(
        "-s", "--dbscan", action="store_true", help="run only the dbscan algorithm"
    )

    if len(sys.argv) == 1:
        print("\nPlease provide command line arguments")
        print("Choose one of the following:")
        print("-d or --dataset {./dataset.csv}")
        print("-g or --generate to generate several dataset types\n")
        print("Choose one of the following:")
        print("-e or --experiment to run all algorithms")
        print("-m or --kmeans to run only the k-means algorithm")
        print("-o or --kmedoid to run only the k-medoid algorithm")
        print("-s or --dbscan to run only the dbscan algorithm\n")
        return -1

    args = parser.parse_args()

    if args.dataset:
        print("Path to csv: {0}".format(args.dataset))

    if args.generate:
        print("The following datasets will be generated:")
        print("\tlist some datasets")

    return args


main()