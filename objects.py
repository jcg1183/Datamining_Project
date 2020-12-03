import settings
from dbscan import dbscan
import KBRAIN

# ***************************************************************
# Class:            experiment
# Variables/input:  list[objects.dataset]: generated datasets
#                   list[string]: names of algorithms
# Output:           returns an experiment object
# Usage/Purpose:    Class contains a list of datasets to work on
#                   and a dictionary of results by algorithm.
# ***************************************************************
class experiment:
    def __init__(self, datasets, algorithms):
        self.datasets = datasets
        self.algorithms = algorithms

        self.results = {}

        for algo in algorithms:
            self.results[algo] = []

        print("Experiment created")


# ***************************************************************
# Class:            algorithm
# Variables/input:  string: name of the algorithm
# Output:           returns an algorithm object
# Usage/Purpose:    Class contains an algorithm name and a
#                   description of the algorithm.
# ***************************************************************
class algorithm:
    def __init__(self, name):
        self.name = name
        self.description = settings.description[name]
        print("Algorithm created {0}".format(name))


# ***************************************************************
# Class:            dataset
# Variables/input:  string: name of the dataset
#                   pandas dataframe: dataset
# Output:           returns a dataset object
# Usage/Purpose:    Class contains the dataset name, datapoints,
#                   and distance matrix.
# ***************************************************************
class dataset:
    def __init__(self, name, df):
        self.name = name
        self.df = df
        self.distanceArray = 0

    def __str__(self):
        return hex(id(self))
