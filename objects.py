import settings
from dbscan import dbscan
import KBRAIN


class experiment:
    def __init__(self, datasets, algorithms):
        self.datasets = datasets
        self.algorithms = algorithms
        self.functions = {}

        for algo in algorithms:
            if algo == "DBSCAN":
                self.functions[algo] = dbscan
            if algo == "k-means" or algo == "k-medoid":
                self.functions[algo] = KBRAIN

        self.results = {}

        for algo in algorithms:
            self.results[algo] = []

        print("Experiment created")


class algorithm:
    def __init__(self, name):
        self.name = name
        self.description = settings.description[name]
        print("Algorithm created {0}".format(name))


class dataset:
    def __init__(self, name, df):
        self.name = name
        self.df = df
        self.distanceArray = 0
    def __str__(self):
        return hex(id(self))
