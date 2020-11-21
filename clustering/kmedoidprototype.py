# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 13:27:31 2020

@author: 98sco
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from random import randint

def euclid_dist(a, b):
    # calculate the eucludean distance between two points
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def compute_new_medoids(med, cluster):
    temp = [med,0]
    
    # for each point in the cluster...
    for p in cluster:
        # if the point is the medoid,
        # continue (no need to calculate and add zero)
        if p == med:
            continue
        # add the euclidean distance between the point and the medoid
        temp[1] += euclid_dist(med, p)
    
    i = len(cluster)
    # while there are points left...
    while i > 0:
        dist = 0
        # for point in cluster...
        for p in cluster:
            # if the point is the current temp medoid
            # continue (no need to calculate and add zero)
            if p == cluster[i - 1]:
                continue
            # add the euclidean distance between the point and the temp medoid
            dist += euclid_dist(cluster[i - 1], p)
        # if the total distance of the temp medoid is less than the current medoid
        # save the distance and index of the new medoid
        if dist < temp[1]:
            temp[0] = cluster[i - 1]
            temp[1] = dist
        i -= 1

    # return the new medoid
    return temp[0]
        
def kmedoid_cluster_prototype(k, points, medoids=None):
    # Base Cases
    if k == 0:
        return None
    if k == 1 or k == len(pts):
        return points
    
    # initial medoid error management
    if medoids != None:
        if len(medoids) != k:
            print("ERROR: Number of provided medoids does not equal k")
            return
    # generate random medoids if none are input
    else:
        num_pts = len(points) - 1
        init = []
        medoids = []
        clusters = []
        
        # random centroid selection with hash-table style collision management
        for i in range(0,k):
            temp = randint(0,num_pts)
            while temp in init:
                temp = (temp + 1) % num_pts
            init.append(temp)
            medoids.append(points[temp])
    
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
                dist = euclid_dist(pt,medoids[n])
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
            # keep the corresponding medoid 
            if clusters[n] == []:
                new_ctrs.append(medoids[n])
            # else, generate a new medoid based its cluster
            else:
                new_ctrs.append(compute_new_medoids(medoids[n], clusters[n]))
                
        # if the new medoids are the same as the current medoids
        # exit the loop
        if new_ctrs == medoids:
            break
        # else, set the new medoids and continue
        else:
            medoids = new_ctrs
            
    # return the final clusters as a list of lists
    return clusters

# small testing batch
pts = [[2,10],[2,5],[8,4],[5,8],[7,5],[6,4],[1,2],[4,9]]

for i in range(2,9):
    print("K =",i)
    output = kmedoid_cluster_prototype(i, pts)

    for thing in output:
        print(thing)
    print()