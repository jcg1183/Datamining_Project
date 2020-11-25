#!/usr/bin/env python

import argparse
import sys
import settings
from objects import experiment, dataset
from dbscan import dbscan
import pandas as pd
from sklearn import datasets


def main():
    args = run_parser()

    datasets = ready_datasets(args)

    exp = experiment(datasets, settings.algorithms)

    run_experiment(exp)
    # exp1 = experiment(str(args.numruns))


def run_experiment(exp):
    for algo in exp.algorithms:
        for ds in exp.datasets:
            for num in settings.numSamples:
                for i in range(1, settings.numRuns + 1):

                    if algo == dbscan:
                        for eps in settings.epsilons:
                            for mp in settings.minPts:
                                results = dbscan(ds, num, eps, mp)

                                exp.results[algo].append(ds.name, num, i, results)


def ready_datasets(args):
    datasetReturn = []

    if args.dataset:
        dfCSV = pd.read_csv(args.dataset, columns=["x1", "x2"])
        datasetReturn.append(dataset(args.dataset, dfCSV))

        print("dataset read from {0}".format(args.dataset))
        print(dfCSV.head(5))

    if args.generate:
        for name in settings.datasetTypes:
            datasetReturn.append(dataset(name, build_dataset(name)))

    return datasetReturn


def build_dataset(name):
    # build all the dataset types here
    df = pd.DataFrame()

    if name == "circles":
        noisy_circles = datasets.make_circles(
            n_samples=numSamples, factor=0.5, noise=0.05
        )

        df = pd.DataFrame(noisy_circles[0], columns=["x1", "x2"])

        df["y"] = noisy_circles[1]

        print("circles dataset generated")
        print(df.head(5))

    return df


def run_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d", "--dataset", action="store", help="path to a csv dataset {./dataset.csv}"
    )
    parser.add_argument(
        "-g", "--generate", action="store_true", help="generate all dataset types"
    )

    if len(sys.argv) == 1:
        print("\nPlease provide command line arguments")
        print("-d or --dataset {./dataset.csv}")
        print("-g or --generate to generate several dataset types\n")
        exit()

    args = parser.parse_args()

    if args.dataset:
        print("Path to csv: {0}".format(args.dataset))

    if args.generate:
        print("The following datasets will be generated:")
        print("\tlist some datasets")

    return args


main()