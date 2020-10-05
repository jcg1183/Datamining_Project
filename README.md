# Coupons & Consumers
# The Green Team

Joshua Greene  
Jared Scott Phillips

UTSA Fall 2020

In this data mining project, we implement three data mining algorithms and compare their performance to the same algorithms from common libraries.  We also apply the algorithms to a sporting goods store's data and present the results.

## Milestones

```  
Project Proposal                  due 10-09-2020 (in progress)  
Progress Report                   due 10-26-2020 (pending)  
Final Report for class            due 11-30-2020 (pending)  
Project Presentation for class    due 11-30-2020 (pending)  
Presentation for Store Owners     due 12-04-2020 (pending)  
```

## Algorithms

We chose to implement the FP-Tree algorithm for association pattern mining, k-means clustering to group customers into outdoor sporting activity categories, and a support vector machine for coupon use prediction.

## Datasets

Our project performs analysis on transactional data from a small sporting goods store.  To develop and test the algorithms, we used a [small grocery store transaction dataset](https://www.kaggle.com/heeraldedhia/groceries-dataset) from Kaggle.  

The sporting goods store data will not be made publicly available.

## Our Libraries

Each algorithm will be packaged as its own library and will come with a preprocessing script that will convert a csv file into the appropriate format for the algorithm.  Look in each library folder for a readme specific to that library.

The run_project.py script will call each algorithm and provide a results file with output from the algorithm and performance metrics.
