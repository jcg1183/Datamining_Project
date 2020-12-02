import pandas as pd


def save_results(resultsDF):
    resultsDF.drop(["cluster_list", "dataset"], axis=1).to_csv(
        r"results.csv", index=False
    )


def compile_results(exp):
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

    # dbscan ds.name, num, i, eps, mp, results
    # kmeans/kmedoid ds.name, num, i, numClusters, results
    for algo in exp.results.keys():
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
