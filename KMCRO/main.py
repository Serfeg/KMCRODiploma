import math as m
import random as r
import matplotlib.pyplot as plt
import kmeans

# Пример из excel файла
# dataSet = [[5, 0],
# [5, 2],
# [3, 1],
# [0, 4],
# [2, 1],
# [4, 2],
# [2, 2],
# [2, 3],
# [1, 3],
# [5, 4]]
# cluster = [1, 2, 1, 2, 1, 2, 2, 2, 1, 2]

# Количество кластеров и точек
k = 3
n = 1000
# Рандомный датасет на 1000 точек
dataSet = [[r.randint(-15, 15) for i in range(2)] for j in range(n)]

# Рандомный кластер на длину датасета
cluster = [r.randint(1, k) for i in range(len(dataSet))]

cluster, centroid, sse, iter = kmeans.kMeans(dataSet, cluster, len(dataSet), k)

print(f"Count of Cluster: {k}\nCentroid: {centroid}\nSSE: {sse}\nCount of Iteration: {iter}")

for i in range(len(dataSet)):
    if cluster[i] == 1:
        plt.scatter(dataSet[i][0], dataSet[i][1], c='red', marker='o')
    elif cluster[i] == 2:
        plt.scatter(dataSet[i][0], dataSet[i][1], c='blue', marker='^')
    elif cluster[i] == 3:
        plt.scatter(dataSet[i][0], dataSet[i][1], c='green', marker='s')
    elif cluster[i] == 4:
        plt.scatter(dataSet[i][0], dataSet[i][1], c='pink', marker='p')
    elif cluster[i] == 5:
        plt.scatter(dataSet[i][0], dataSet[i][1], c='orange', marker='d')
    elif cluster[i] == 6:
        plt.scatter(dataSet[i][0], dataSet[i][1], c='purple', marker='*')
    elif cluster[i] == 7:
        plt.scatter(dataSet[i][0], dataSet[i][1], c='lime', marker='H')

for i in range(len(centroid)):
    plt.scatter(centroid[i][0], centroid[i][1], c='black', marker='2', linewidths=5)

plt.grid(True)
plt.show()
