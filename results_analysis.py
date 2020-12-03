import pandas as pd

# ***************************************************************
# Function:         save_results
# Variables/input:  pandas dataframe: results of each experiment
# Output:           writes results to .csv file
# Usage/Purpose:    Function writes the results of all experiments
#                   to .csv file.
# ***************************************************************
def save_results(resultsDF):
    resultsDF.drop(["cluster_list", "dataset"], axis=1).to_csv(
        r"results.csv", index=False
    )


# ***************************************************************
# Function:         compile_results
# Variables/input:  objects.experiment
# Output:           pandas dataframe: resultsDF
# Usage/Purpose:    Function creates a summary of all experiments
#                   their parameters, and results.
# ***************************************************************
def compile_results(exp):
    # set up new dataframe
    resultsDF = pd.DataFrame(
        columns=[
            "algo",
            "dataset_type",
            "num_pts",
            "trial_num",
            "epsilon",
            "min_pts",
            "k",
            "dataset",
            "cluster_list",
        ]
    )

    # loop through all results in the experiment
    for algo in exp.results.keys():
        # write results summary of dbscan algorithms
        if algo == "DBSCAN" or algo == "sklearn_dbscan":
            for result in exp.results[algo]:
                resultsDF = resultsDF.append(
                    {
                        "algo": algo,
                        "dataset_type": result[0],
                        "num_pts": result[1],
                        "trial_num": result[2],
                        "epsilon": result[3],
                        "min_pts": result[4],
                        "k": -1,
                        "dataset": next(x for x in exp.datasets if x.name == result[0]),
                        "cluster_list": result[5],
                    },
                    ignore_index=True,
                )
        else:
            # write results to k-* algorithms
            for result in exp.results[algo]:
                # kmeans/kmedoid ds.name, num, i, numClusters, results

                resultsDF = resultsDF.append(
                    {
                        "algo": algo,
                        "dataset_type": result[0],
                        "num_pts": result[1],
                        "trial_num": result[2],
                        "epsilon": -1,
                        "min_pts": -1,
                        "k": result[3],
                        "dataset": next(x for x in exp.datasets if x.name == result[0]),
                        "cluster_list": result[4],
                    },
                    ignore_index=True,
                )

    return resultsDF
