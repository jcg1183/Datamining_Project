import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from random import randint

def euclid_dist(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def two_dimension_mean(a):
    x = []
    y = []
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
    
    if centroids != None:
        if len(centroids) != k:
            print("ERROR: Number of provided centroids does not equal k")
            return
    else:
        num_pts = len(points) - 1
        init = []
        centroids = []
        clusters = []
        
        for i in range(0,k):
            temp = randint(0,num_pts)
            while temp in init:
                temp = (temp + 1) % num_pts
            init.append(temp)
            centroids.append(points[temp])
    
    while(1):
        clusters = []
        for i in range(0,k):
            clusters.append([])
        temp = [1024,0]
        for pt in points:
            for n in range(0,k):
                dist = euclid_dist(pt,centroids[n])
                if dist < temp[0]:
                    temp[0] = dist
                    temp[1] = n
            clusters[temp[1]].append(pt)
            temp = [1024,0]   
        
        new_ctrs = []
        
        for n in range(0,k):
            if clusters[n] == []:
                new_ctrs.append(centroids[n])
            else:
                new_ctrs.append(two_dimension_mean(clusters[n]))
        
        if new_ctrs == centroids:
            break
        else:
            centroids = new_ctrs
    
    return clusters

pts = [[2,10],[2,5],[8,4],[5,8],[7,5],[6,4],[1,2],[4,9]]

for i in range(2,9):
    print("K =",i)
    output = kmeans_cluster_prototype(i, pts)

    for thing in output:
        print(thing)
    print()