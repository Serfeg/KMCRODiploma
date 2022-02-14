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
    k = 4

    # Рандомный кластер на длину датасета
    originalCluster = [r.randint(1, k) for i in range(len(dataSet))]
    # newCluster, centroid, sse, countIter = kmeans.kMeans(dataSet, originalCluster, k)

    #dfCentroid = pd.DataFrame()

    # df['Cluster'] = newCluster
    # for i in range(len(centroid)):
    #     dfCentroid['Cluster '+str(i + 1)] = centroid[i]

    # print(f"Count of Cluster: {k}\nSSE: {sse}\nCount of Iteration: {countIter}\n"
    #       f"Centroid:\n{dfCentroid}\n\nDataSet with Clusters:\n{df}\n\n"
    #       f"Confusion Matrix:\n{confusion_matrix(originalCluster, newCluster)}\nNew Cluster: {newCluster}")

    newCluster, centroid, sse, countIter = kmeans.kMeansWithCos(dataSet, originalCluster, k)

    print(f"Count of Cluster: {k}\nSSE: {sse}\nCount of Iteration: {countIter}\n"
          f"Centroid:\n{dfCentroid}\nNew Cluster: {newCluster}")

