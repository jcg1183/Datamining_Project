import settings


class experiment:
    def __init__(self, datasets, algorithms):
        self.datasets = datasets
        self.algorithms = []

        for algo in algorithms:
            self.algorithms.append(algorithm(algo))

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