import math as m
import random as r

import matplotlib as plot


def findCentroid(dataSet, dataSetColumn, cluster, kNumber):
    sum = 0
    z = 0
    for i in range(len(dataSet)):
        if cluster[i] == kNumber:
            z += 1
            sum += dataSet[i][dataSetColumn]
    return sum / z


def euclideanDistance(dataSetRow, centroid):
    sum = 0
    for i in range(len(dataSetRow)):
        sum += (dataSetRow[i]-centroid[i])**2
    return sum


def countSse(euclidDist):
    sum = 0
    for i in range(len(euclidDist)):
        sum += min(euclidDist[i])
    return sum

n = 2

dataSet = [[5, 0],
           [5, 2],
           [3, 1],
           [0, 4],
           [2, 1],
           [4, 2],
           [2, 2],
           [2, 3],
           [1, 3],
           [5, 4]]
lenDs = len(dataSet)
#cluster = [r.randint(1,n) for i in range(lenDs)]
cluster = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]


centroid = [[findCentroid(dataSet, col, cluster, kNumber+1) for col in range(len(dataSet[0]))] for kNumber in range(n)]
euclidDist = [[euclideanDistance(dataSet[j], centroid[i]) for i in range(len(centroid))] for j in range(lenDs)]
newClust = [euclidDist[i].index(min(euclidDist[i]))+1 for i in range(len(euclidDist))]
sse = countSse(euclidDist)
print(f"Dataset: {dataSet}\nCount of Cluster: {n}\nRandom Cluster: {cluster}\nCentroid: {centroid}\nNew Cluster: {newClust}\nSSE: {sse}")

