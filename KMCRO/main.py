import math as m
import random as r
import matplotlib.pyplot as plt
import kmeans
from scipy.stats.contingency import crosstab
import pandas as pd


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
    dataSet = makeDataSet("11_33_37_42.txt")
    df = pd.read_csv('11_33_37_42.txt', delimiter="\t")
    
    # Количество кластеров и точек
    k = 4
    # Рандомный кластер на длину датасета
    originalCluster = [r.randint(1, k) for i in range(len(dataSet))]
    newCluster, centroid, sse, countIter = kmeans.kMeans(dataSet, originalCluster, len(dataSet), k)

    dfCentroid = pd.DataFrame()

    df['Cluster'] = newCluster
    for i in range(len(centroid)):
        dfCentroid['Cluster '+str(i+1)] = centroid[i]

    print(f"Count of Cluster: {k}\nSSE: {sse}\nCount of Iteration: {countIter}\n"
          f"Centroid:\n{dfCentroid}\nDataSet with Clusters:\n{df}")

    # for i in range(len(dataSet)):
    #     if cluster[i] == 1:
    #         plt.scatter(dataSet[i][0], dataSet[i][1], c='red', marker='o')
    #     elif cluster[i] == 2:
    #         plt.scatter(dataSet[i][0], dataSet[i][1], c='blue', marker='^')
    #     elif cluster[i] == 3:
    #         plt.scatter(dataSet[i][0], dataSet[i][1], c='green', marker='s')
    #     elif cluster[i] == 4:
    #         plt.scatter(dataSet[i][0], dataSet[i][1], c='pink', marker='p')
    #     elif cluster[i] == 5:
    #         plt.scatter(dataSet[i][0], dataSet[i][1], c='orange', marker='d')
    #     elif cluster[i] == 6:
    #         plt.scatter(dataSet[i][0], dataSet[i][1], c='purple', marker='*')
    #     elif cluster[i] == 7:
    #         plt.scatter(dataSet[i][0], dataSet[i][1], c='lime', marker='H')
    #
    # for i in range(len(centroid)):
    #     plt.scatter(centroid[i][0], centroid[i][1], c='black', marker='2', linewidths=5)
    #
    #
    # plt.grid(True)
    # plt.show()
