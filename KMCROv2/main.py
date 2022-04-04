import math as m
import random as r
import matplotlib.pyplot as plt
import kmeans
import cro
import pandas as pd
from sklearn.metrics import confusion_matrix


def makeDataSet(filename):
    dataSet = []
    eps = []
    file = open(filename)
    s = file.readlines()[1:]
    for i in s:
        dataSet.append(i.split())
    file.close()
    for i in range(len(dataSet)):
        for j in range(len(dataSet[i])):
            dataSet[i][j] = float(dataSet[i][j])
    for i in range(len(dataSet)):
        eps.append(int(dataSet[i][0]))
    for i in range(len(dataSet)):
        dataSet[i].pop(0)
    return dataSet, eps

def makeEpsCluster(fileName, eps):
    epsCluster = []
    if fileName == '33_42.txt':
        for i in range(len(eps)):
            str1 = str(eps[i])[0:2]
            if str1 == '33':
                epsCluster.append(1)
            elif str1 == '42':
                epsCluster.append(2)
    elif fileName == '33_37_42.txt':
        for i in range(len(eps)):
            str1 = str(eps[i])[0:2]
            if str1 == '33':
                epsCluster.append(1)
            elif str1 == '37':
                epsCluster.append(2)
            elif str1 == '42':
                epsCluster.append(3)
    elif fileName == '11_33_37_42.txt':
        for i in range(len(eps)):
            str1 = str(eps[i])[0:2]
            if str1 == '11':
                epsCluster.append(1)
            elif str1 == '33':
                epsCluster.append(2)
            elif str1 == '37':
                epsCluster.append(3)
            elif str1 == '42':
                epsCluster.append(4)
    elif fileName == 'total_sample_no_empties.txt':
        for i in range(len(eps)):
            str1 = str(eps[i])[0:2]
            if str1 == '11':
                epsCluster.append(1)
            elif str1 == '13':
                epsCluster.append(2)
            elif str1 == '21':
                epsCluster.append(3)
            elif str1 == '33':
                epsCluster.append(4)
            elif str1 == '37':
                epsCluster.append(5)
            elif str1 == '42':
                epsCluster.append(6)
            elif str1 == '45':
                epsCluster.append(7)
    return epsCluster


if __name__ == "__main__":
    print('Введите номер файла.\n\t'
          '1. 33_42\n\t'
          '2. 33_37_42\n\t'
          '3. 11_33_37_42\n\t'
          '4. total_sample_no_empties')
    fileNumber = int(input())
    if fileNumber == 1:
        fName = '33_42.txt'
    elif fileNumber == 2:
        fName = '33_37_42.txt'
    elif fileNumber == 3:
        fName = '11_33_37_42.txt'
    elif fileNumber == 4:
        fName = 'total_sample_no_empties.txt'
    #fName = '33_42.txt'
    dataSet, eps = makeDataSet(fName)
    epsCluster = makeEpsCluster(fName, eps)
    for i in range(len(dataSet)):
        sum = 0
        for j in range(len(dataSet[i])):
            sum += dataSet[i][j] ** 2
        sum = m.sqrt(sum)
        for j in range(len(dataSet[i])):
            dataSet[i][j] *= 1/sum
    #print(min(min(dataSet)), max(max(dataSet)))
    #dataSet = [[dataSet[i][j] / len(dataSet) for j in range(len(dataSet[i]))] for i in range(len(dataSet))]
    df = pd.read_csv(fName, delimiter="\t")

    # Количество кластеров и точек
    print("Введите количество кластеров")
    k = int(input())
    print("Введите количество итераций для CRO")
    iterCRO = int(input())


    # Рандомный кластер на длину датасета
    originalCluster = [r.randint(1, k) for i in range(len(dataSet))]

    #newCluster, centroid, sse, countIterKMeans = kmeans.kMeans(dataSet, originalCluster, k)
    newCluster, centroid, sse, countIterKMeans = kmeans.kMeansWithCos(dataSet, originalCluster, k)
    #newCluster, centroid, sse, countIterKMeans = kmeans.kMeansWithCosRandomCentroid(dataSet, originalCluster, k)
    #newCluster, centroid, sse, countIterKMeans = kmeans.kMeansRandom(dataSet, originalCluster, k)

    dfCentroid = pd.DataFrame()

    for i in range(len(centroid)):
        dfCentroid['Cluster ' + str(i + 1)] = centroid[i]
    #fitness = kmeans.fitnessEuclidDist(dataSet, newCluster, centroid, k)
    fitness = kmeans.fitnessCosWithDist(dataSet, newCluster, centroid, k)
    print(f"Fitness K-means: {fitness}")

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

    df['Cluster'] = newCluster

    print(f"Count of Cluster: {k}\nSSE: {sse}\nCount of Iteration K-means: {countIterKMeans}\n"
          f"Fitness CRO: {fitness}\n"
          f"Centroid:\n{dfCentroid}\n\n"
          f"DataSet with Clusters:\n{df}\n\n"
          f"Confusion Matrix:\n{confusion_matrix(epsCluster, newCluster)}")

