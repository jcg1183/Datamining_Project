# Bootleg Clusters
# The Green Team

Joshua Greene  
Jared Scott Phillips

UTSA Fall 2020

In this data mining project, we implemented three clustering algorithms and benchmarked their performance against existing programming libraries.

## Milestones

```  
Project Proposal                  due 10-05-2020 (completed)
Algorithm 0: FP-Growth            (completed)  
Progress Report                   due 10-26-2020 (completed)
Algorithm 1: K-Means              (completed)
Algorithm 2: PAM/K-Medoid         (completed)
Algorithm 3: DBSCAN               (completed)
Final Report for class            due 12-2-2020 (completed)  
Project Presentation for class    due 12-2-2020 (completed)  
Presentation for Store Owners     due 12-04-2020 (cancelled)  
```

## Algorithms

We chose to implement the K-Means, K-Medoid, and DBSCAN clustering algorithms.

## Datasets

We are utilizing sciki-learn.datasets and Numpy for dataset generation, the project additionally can take in user-provided datasets

## Our Implementation

The clusters.py script will call each algorithm and provide a results file with output from the algorithm and performance metrics.

## User Manual

Installation: Clone the repository to any directory of your choosing. All files (save for those which are archived) must be in the same directory for Bootleg Clusters to operate

Operation: Bootleg Clusters is run from the command-line using clusters.py -> "python3 clusters.py [options]"

  There is a list of options to customize the execution:
  
    '-d' or '--dataset' [path_to.csv]: specify a .csv file for clustering
    '-g' or '--generate': Generate all dataset types for clustering
    '-e' or '--experiment': Run all clustering algorithms on the datasets
    '-m' or '--kmeans': Run only the K-Means algorithm
    '-o' or '--kmedoids': Run only the K-Medoids algorithm
    '-s' or '--dbscan': Run only the DBSCAN algorithm
    
  Upon completion, Bootleg Clusters will print the results of the experiment in the console, including the algorithm, options, dataset, and accuracy scores
  
Settings: Custom selection of dataset types, sample ranges, number of runs, and epsilons and minimum points (for DBSCAN) can be set within settings.py

  Note - Bootleg Clusters' completion time is dependent on the maxSamples variable in settings.py, the runtime complexity for calculating the distance matrix for each
  dataset is roughly O(2^n) per dataset where n is maxSamples.
