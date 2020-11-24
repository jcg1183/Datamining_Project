#!/usr/bin/env python

import argparse
import sys
import settings
from objects import experiment, dataset
import pandas as pd
from sklearn import datasets


def main():
    args = run_parser()

    datasets = ready_datasets(args)

    # exp1 = experiment(str(args.numruns))


def ready_datasets(args):
    datasetReturn = []

    if args.dataset:
        dfCSV = pd.read_csv(args.dataset, columns=["x1", "x2"])
        datasetReturn.append(dataset(args.dataset, dfCSV))

        print("dataset read from {0}".format(args.dataset))
        print(dfCSV.head(5))

    if args.generate:
        for name in settings.datasetTypes:
            datasetReturn.append(
                dataset(name, build_dataset(name, int(args.numsamples)))
            )

    return datasetReturn


def build_dataset(name, numSamples):
    # build all the dataset types here
    df = pd.DataFrame()

    if name == "circles":
        noisy_circles = datasets.make_circles(
            n_samples=numSamples, factor=0.5, noise=0.05
        )

        df = pd.DataFrame(noisy_circles[0], columns=["x1", "x2"])

        df["y"] = noisy_circles[1]

        df["visited"] = 0
        df["cluster"] = -1
        df["neighbors"] = [[] for _ in range(numSamples)]

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

    parser.add_argument(
        "-r",
        "--numruns",
        action="store",
        help="number of runs per algorithm",
        default=5,
    )

    parser.add_argument(
        "-s",
        "--numsamples",
        action="store",
        help="number of samples per dataset",
        default=500,
    )

    if len(sys.argv) == 1:
        print("\nPlease provide command line arguments")
        print("-d or --dataset {./dataset.csv}")
        print("-g or --generate to generate several dataset types")
        print("-r or --numruns {int}")
        print("-s or --numsamples {int}\n")
        exit()

    args = parser.parse_args()

    if args.dataset:
        print("Path to csv: {0}".format(args.dataset))

    if args.generate:
        print("The following datasets will be generated:")
        print("\tlist some datasets")

    if int(args.numruns) > 0:
        print("Each algorithm will be run {0} times.".format(args.numruns))
    else:
        print("\nInvalid number of runs.\n")
        exit()

    if int(args.numsamples) > 0:
        print("Each dataset will have {0} samples.".format(args.numsamples))
    else:
        print("\nInvalid number of samples.\n")
        exit()

    return args


main()