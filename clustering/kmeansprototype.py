import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from random import randint

def euclid_dist(a, b):
    # calculate the eucludean distance between two points
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def two_dimension_mean(a):
    x = []
    y = []
    # splits x and y elements to calculate mean of all points
    for point in a:
        x.append(point[0])
        y.append(point[1])
    return [np.mean(x), np.mean(y)]
        
def kmeans_cluster_prototype(k, points, centroids=None):
    # Base Cases
    if k == 0:
        return None
    if k == 1 or k == len(pts):
        return points
    
    # initial centroid error management
    if centroids != None:
        if len(centroids) != k:
            print("ERROR: Number of provided centroids does not equal k")
            return
    # generate random centroids if none are input
    else:
        num_pts = len(points) - 1
        init = []
        centroids = []
        clusters = []
        # random centroid selection with hash-table style collision management
        for i in range(0,k):
            temp = randint(0,num_pts)
            while temp in init:
                temp = (temp + 1) % num_pts
            init.append(temp)
            centroids.append(points[temp])
    
    while(1):
        # generate empty lists for k-clusters
        clusters = []
        for i in range(0,k):
            clusters.append([])
        temp = [1024,0]
        # for each point...
        for pt in points:
            for n in range(0,k):
                # calculate the euclidean distance between the point
                # and each centroid[0,...,k]
                dist = euclid_dist(pt,centroids[n])
                # if the distace is shorter than the current saved centroid
                # save the new distance and centroid index
                if dist < temp[0]:
                    temp[0] = dist
                    temp[1] = n
            # add the current point to the closest centroid's cluster
            clusters[temp[1]].append(pt)
            # reset and continue
            temp = [1024,0]   
        
        new_ctrs = []
        
        # for all clusters...
        for n in range(0,k):
            # if the cluster is empty,
            # keep the corresponding centroid
            if clusters[n] == []:
                new_ctrs.append(centroids[n])
            # else, generate a new centroid based its cluster
            else:
                new_ctrs.append(two_dimension_mean(clusters[n]))
        
        # if the new centroids are the same as the current centroids
        # exit the loop
        if new_ctrs == centroids:
            break
        # else, set the new centroids and continue
        else:
            centroids = new_ctrs
    
    # return the final clusters as a list of lists
    return clusters

# small testing batch
pts = [[2,10],[2,5],[8,4],[5,8],[7,5],[6,4],[1,2],[4,9]]

for i in range(2,9):
    print("K =",i)
    output = kmeans_cluster_prototype(i, pts)

    for thing in output:
        print(thing)
    print()