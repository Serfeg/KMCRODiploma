import math as m
import random as r
import matplotlib.pyplot as plt
import kmeans
from scipy.stats.contingency import crosstab


if __name__ == "__main__":
    dataSet = []
    with open("11_33_37_42.txt", "r") as file:
        for line in file:
            dataSet.append(line.split())
        file.close()
    # Пример из excel файла
    # dataSet = [[5, 0, 5, -1],
    #            [5, 2, 2, 0],
    #            [3, 1, 1, -6],
    #            [0, 4, 10, 10],
    #            [2, 1, 20, 9],
    #            [4, 2, 5, -5],
    #            [2, 2, 6, 56],
    #            [2, 3, 8, -9],
    #            [1, 3, 6, 1],
    #            [5, 4, 9, 0]]
    # cluster = [1, 2, 1, 2, 1, 2, 2, 2, 1, 2]
    # Количество кластеров и точек
    #k = 7
    #n = 1000
    # Рандомный датасет на 1000 точек
    #dataSet = [[r.randint(-15, 15) for i in range(4)] for j in range(n)]

    # Рандомный кластер на длину датасета
    #originalCluster = [r.randint(1, k) for i in range(len(dataSet))]
    #newCluster, centroid, sse, iter = kmeans.kMeans(dataSet, originalCluster, len(dataSet), k)

    #print(f"Count of Cluster: {k}\nCentroid: {centroid}\nSSE: {sse}\nCount of Iteration: {iter}")
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
