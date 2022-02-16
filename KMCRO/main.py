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
    dataSet = makeDataSet("11_33_37_42.txt")
    df = pd.read_csv('11_33_37_42.txt', delimiter="\t")
    # Количество кластеров и точек
    print("Введите количество кластеров")
    k = int(input())
    print("Введите количество итераций для CRO")
    iterCRO = int(input())
    # Рандомный кластер на длину датасета
    originalCluster = [r.randint(1, k) for i in range(len(dataSet))]
    # dataSet = [
    #     [5, 0],
    #     [5, 2],
    #     [3, 1],
    #     [0, 4],
    #     [2, 1],
    #     [4, 2],
    #     [2, 2],
    #     [2, 3],
    #     [1, 3],
    #     [5, 4]
    # ]
    # originalCluster = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    #originalCluster, centroid, sse, countIter = kmeans.kMeans(dataSet, originalCluster, k)
    newCluster, centroid, sse, countIterKMeans = kmeans.kMeansWithCos(dataSet, originalCluster, k)
    dfCentroid = pd.DataFrame()

    df['Cluster'] = newCluster
    for i in range(len(centroid)):
        dfCentroid['Cluster ' + str(i + 1)] = centroid[i]

    countClusterKMeans = []
    for i in range(k):
        g = 0
        for j in newCluster:
            if j == i + 1:
                g += 1
        countClusterKMeans.append(g)

    fitness = kmeans.fitnessCosWithDist(dataSet, newCluster, centroid, k)
    countIterCRO = 0

    while True:
        countIterCRO += 1
        croFitness = []
        croList = []

        #singleMoleculeCollision
        cluster1 = cro.singleMoleculeCollision(len(dataSet), k)
        croFitness.append(kmeans.fitnessCosWithDist(dataSet, cluster1, centroid, k))
        croList.append(cluster1)

        #singleMoleculeDecomposition
        clusterOdd, clusterEven = cro.singleMoleculeDecomposition(len(dataSet), k)
        fitnessOdd = kmeans.fitnessCosWithDist(dataSet, clusterOdd, centroid, k)
        fitnessEven = kmeans.fitnessCosWithDist(dataSet, clusterEven, centroid, k)
        if fitnessOdd >= fitnessEven:
            croFitness.append(fitnessOdd)
            croList.append(clusterOdd)
        else:
            croFitness.append(fitnessEven)
            croList.append(clusterEven)

        #intermolecularCollision
        clusterPhi1, clusterPhi2 = cro.intermolecularCollision(len(dataSet), k)
        fitnessPhi1 = kmeans.fitnessCosWithDist(dataSet, clusterPhi1, centroid, k)
        fitnessPhi2 = kmeans.fitnessCosWithDist(dataSet, clusterPhi2, centroid, k)
        if fitnessPhi1 >= fitnessPhi2:
            croFitness.append(fitnessPhi1)
            croList.append(clusterPhi1)
        else:
            croFitness.append(fitnessPhi2)
            croList.append(clusterPhi2)

        #intermolecularSynthesis
        cluster2 = cro.intermolecularSynthesis(len(dataSet), k)
        croFitness.append(kmeans.fitnessCosWithDist(dataSet, cluster2, centroid, k))
        croList.append(cluster2)

        if fitness < max(croFitness):
            fitness = max(croFitness)
            newCluster = croList[croFitness.index(max(croFitness))]

        if countIterCRO == iterCRO:
            break

    countClusterCRO = []
    for i in range(k):
        g = 0
        for j in newCluster:
            if j == i + 1:
                g += 1
        countClusterCRO.append(g)

    print(f"Count of Cluster: {k}\nSSE: {sse}\nCount of Iteration K-means: {countIterKMeans}\n"
          f"Fitness: {fitness}\n"
          f"Centroid:\n{dfCentroid}\n\n"
          f"DataSet with Clusters:\n{df}\n\n"
          f"Count Cluster K-means {countClusterKMeans}\n"
          f"Count Cluster CRO: {countClusterCRO}\n"
          f"Confusion Matrix:\n{confusion_matrix(originalCluster, newCluster)}")
