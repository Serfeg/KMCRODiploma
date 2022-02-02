import math as m
import random as r

import matplotlib as plot


def randomCluster(dataSet, n):
    for i in range(len(dataSet)):
        dataSet[i][-1] = r.randint(1, n)
    return dataSet


def findCentroid(dataSet, C, col):
    sum = 0
    z = 0
    for i in range(len(dataSet)):
        if dataSet[i][-1] == C:
            z += 1
            sum += dataSet[i][col]
    return sum / z


n = 2

dataSet = [[5, 0, 1],
           [5, 2, 2],
           [3, 1, 1],
           [0, 4, 2],
           [2, 1, 1],
           [4, 2, 2],
           [2, 2, 1],
           [2, 3, 2],
           [1, 3, 1],
           [5, 4, 2]]

Centroid = [[findCentroid(dataSet, j+1, i) for i in range(len(dataSet[0])-1)] for j in range(n)]


# x = [5, 5, 3, 0, 2, 4, 2, 2, 1, 5]
# y = [0, 2, 1, 4, 1, 2, 2, 3, 3, 4]
# n = 2
# K = [r.randint(1,n) for i in range(len(x))]
# K = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
