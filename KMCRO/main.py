import math as m
import random as r
import matplotlib.pyplot as plt
import kmeans
import cro
from scipy.stats.contingency import crosstab
import pandas as pd
from sklearn.metrics import confusion_matrix


def makeDataSet(filename):
    dataSet = []
    file = open(filename)
    s = file.readlines()[1:]
    for i in s:
        dataSet.append(i.split())
    file.close()
    for i in range(len(dataSet)):
        for j in range(len(dataSet[i])):
            dataSet[i][j] = float(dataSet[i][j])
    for i in range(len(dataSet)):
        dataSet[i].pop(0)
    return dataSet


if __name__ == "__main__":
    #dataSet = makeDataSet("11_33_37_42.txt")
    #df = pd.read_csv('11_33_37_42.txt', delimiter="\t")
    # Количество кластеров и точек
    k = 2
    # Рандомный кластер на длину датасета
    #originalCluster = [r.randint(1, k) for i in range(len(dataSet))]
    dataSet = [
        [0.5, 0.0],
        [0.5, 0.2],
        [0.3, 0.1],
        [0.0, 0.4],
        [0.2, 0.1],
        [0.4, 0.2],
        [0.2, 0.2],
        [0.2, 0.3],
        [0.1, 0.3],
        [0.5, 0.4]
    ]
    originalCluster = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    #newCluster, centroid, sse, countIter = kmeans.kMeans(dataSet, originalCluster, k)
    newCluster, centroid, sse, countIter = kmeans.kMeansWithCos(dataSet, originalCluster, k)
    dfCentroid = pd.DataFrame()

    #df['Cluster'] = newCluster
    for i in range(len(centroid)):
        dfCentroid['Cluster ' + str(i + 1)] = centroid[i]

    nK = []
    for i in range(k):
        h = 0
        for j in newCluster:
            if j == i+1:
                h += 1
        nK.append(h)

    fitness = kmeans.fitnessCosWithDist(dataSet, newCluster, centroid, nK)
    print(fitness)

    print(f"Count of Cluster: {k}\nSSE: {sse}\nCount of Iteration: {countIter}\n"
          f"Centroid:\n{dfCentroid}")
          #f"\n\nDataSet with Clusters:\n{df}\n\nFitness: {fitness}\n"
          #f"Confusion Matrix:\n{confusion_matrix(originalCluster, newCluster)}")
