import math as m
import random as r
import kmeans
import cro


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


k = 7

dataSet = makeDataSet("total_sample_no_empties.txt")

originalCluster = [r.randint(1, k) for i in range(len(dataSet))]

f = open('text.txt', 'w')

f.write('Исходный датасет\n')

f.write('\n')

sse = 0
h = 0

allOriginalCentroids = []
allChangedCentroid = []
while h < 1:
    f.write('Итерация №' + str(h + 1) + '\n')
    f.write('Начальные центроиды\n')
    originalCluster = [r.randint(1, k) for i in range(len(dataSet))]

    f.write('CosineSimilarity\n')
    newCluster, centroid, sse, countIterKMeans = kmeans.kMeansWithCos(dataSet, originalCluster, k)
    f.write('Итоговые центроиды\n')
    for i in range(len(centroid)):
        f.write('C' + str(i + 1) + '\t')
        for j in range(len(centroid[i])):
            f.write(str(centroid[i][j]) + '\t')
        f.write('\n')
    f.write('\n')

    f.write('\n')

    f.write('SSE: ' + str(sse) + '\n\n')

    fitness = kmeans.fitnessCos(dataSet, newCluster, centroid, k)
    f.write('Fitness: ' + str(fitness) + '\n')
    changedFitness = False
    countIterCRO = 0
    while True:
        countIterCRO += 1
        croFitness = []
        croList = []

        # singleMoleculeCollision
        cluster1 = cro.singleMoleculeCollision(len(dataSet), k)
        croFitness.append(kmeans.fitnessCos(dataSet, cluster1, centroid, k))
        croList.append(cluster1)

        # singleMoleculeDecomposition
        clusterOdd, clusterEven = cro.singleMoleculeDecomposition(len(dataSet), k)
        fitnessOdd = kmeans.fitnessCos(dataSet, clusterOdd, centroid, k)
        fitnessEven = kmeans.fitnessCos(dataSet, clusterEven, centroid, k)
        if fitnessOdd >= fitnessEven:
            croFitness.append(fitnessOdd)
            croList.append(clusterOdd)
        else:
            croFitness.append(fitnessEven)
            croList.append(clusterEven)

        # intermolecularCollision
        clusterPhi1, clusterPhi2 = cro.intermolecularCollision(len(dataSet), k)
        fitnessPhi1 = kmeans.fitnessCos(dataSet, clusterPhi1, centroid, k)
        fitnessPhi2 = kmeans.fitnessCos(dataSet, clusterPhi2, centroid, k)
        if fitnessPhi1 >= fitnessPhi2:
            croFitness.append(fitnessPhi1)
            croList.append(clusterPhi1)
        else:
            croFitness.append(fitnessPhi2)
            croList.append(clusterPhi2)

        # intermolecularSynthesis
        cluster2 = cro.intermolecularSynthesis(len(dataSet), k)
        croFitness.append(kmeans.fitnessCos(dataSet, cluster2, centroid, k))
        croList.append(cluster2)

        if fitness < max(croFitness):
            fitness = max(croFitness)
            newCluster = croList[croFitness.index(max(croFitness))]
            changedFitness = True

        if countIterCRO == 50:
            if changedFitness:
                f.write('Fitness CRO: ' + str(fitness) + '\n')
            else:
                f.write('k-means посчитал лучшее решение\n')
            break


    f.write('\nEuclidDist\n')
    newCluster, centroid, sse, countIterKMeans = kmeans.kMeans(dataSet, originalCluster, k)
    f.write('Итоговые центроиды\n')
    for i in range(len(centroid)):
        f.write('C' + str(i + 1) + '\t')
        for j in range(len(centroid[i])):
            f.write(str(centroid[i][j]) + '\t')
        f.write('\n')
    f.write('\n')

    f.write('\n')

    f.write('SSE: ' + str(sse) + '\n\n')
    fitness = kmeans.fitnessEuclidDist(dataSet, newCluster, centroid, k)
    f.write('Fitness: ' + str(fitness) + '\n')

    changedFitness = False
    countIterCRO = 0
    while True:
        countIterCRO += 1
        croFitness = []
        croList = []

        # singleMoleculeCollision
        cluster1 = cro.singleMoleculeCollision(len(dataSet), k)
        croFitness.append(kmeans.fitnessEuclidDist(dataSet, cluster1, centroid, k))
        croList.append(cluster1)

        # singleMoleculeDecomposition
        clusterOdd, clusterEven = cro.singleMoleculeDecomposition(len(dataSet), k)
        fitnessOdd = kmeans.fitnessEuclidDist(dataSet, clusterOdd, centroid, k)
        fitnessEven = kmeans.fitnessEuclidDist(dataSet, clusterEven, centroid, k)
        if fitnessOdd >= fitnessEven:
            croFitness.append(fitnessOdd)
            croList.append(clusterOdd)
        else:
            croFitness.append(fitnessEven)
            croList.append(clusterEven)

        # intermolecularCollision
        clusterPhi1, clusterPhi2 = cro.intermolecularCollision(len(dataSet), k)
        fitnessPhi1 = kmeans.fitnessEuclidDist(dataSet, clusterPhi1, centroid, k)
        fitnessPhi2 = kmeans.fitnessEuclidDist(dataSet, clusterPhi2, centroid, k)
        if fitnessPhi1 >= fitnessPhi2:
            croFitness.append(fitnessPhi1)
            croList.append(clusterPhi1)
        else:
            croFitness.append(fitnessPhi2)
            croList.append(clusterPhi2)

        # intermolecularSynthesis
        cluster2 = cro.intermolecularSynthesis(len(dataSet), k)
        croFitness.append(kmeans.fitnessEuclidDist(dataSet, cluster2, centroid, k))
        croList.append(cluster2)

        if fitness > min(croFitness):
            fitness = min(croFitness)
            newCluster = croList[croFitness.index(min(croFitness))]
            changedFitness = True

        if countIterCRO == 50:
            if changedFitness:
                f.write('Fitness CRO: ' + str(fitness) + '\n')
            else:
                f.write('k-means посчитал лучшее решение\n')
            break

    f.write('\nCos+Dist\n')
    newCluster, centroid, sse, countIterKMeans = kmeans.kMeansWithCos(dataSet, originalCluster, k)
    f.write('Итоговые центроиды\n')
    for i in range(len(centroid)):
        f.write('C' + str(i + 1) + '\t')
        for j in range(len(centroid[i])):
            f.write(str(centroid[i][j]) + '\t')
        f.write('\n')
    f.write('\n')

    f.write('\n')

    f.write('SSE: ' + str(sse) + '\n\n')
    fitness = kmeans.fitnessCosWithDist(dataSet, newCluster, centroid, k)
    f.write('Fitness: ' + str(fitness) + '\n')

    countIterCRO = 0
    changedFitness = False
    while True:
        countIterCRO += 1
        croFitness = []
        croList = []

        # singleMoleculeCollision
        cluster1 = cro.singleMoleculeCollision(len(dataSet), k)
        croFitness.append(kmeans.fitnessCosWithDist(dataSet, cluster1, centroid, k))
        croList.append(cluster1)

        # singleMoleculeDecomposition
        clusterOdd, clusterEven = cro.singleMoleculeDecomposition(len(dataSet), k)
        fitnessOdd = kmeans.fitnessCosWithDist(dataSet, clusterOdd, centroid, k)
        fitnessEven = kmeans.fitnessCosWithDist(dataSet, clusterEven, centroid, k)
        if fitnessOdd >= fitnessEven:
            croFitness.append(fitnessOdd)
            croList.append(clusterOdd)
        else:
            croFitness.append(fitnessEven)
            croList.append(clusterEven)

        # intermolecularCollision
        clusterPhi1, clusterPhi2 = cro.intermolecularCollision(len(dataSet), k)
        fitnessPhi1 = kmeans.fitnessCosWithDist(dataSet, clusterPhi1, centroid, k)
        fitnessPhi2 = kmeans.fitnessCosWithDist(dataSet, clusterPhi2, centroid, k)
        if fitnessPhi1 >= fitnessPhi2:
            croFitness.append(fitnessPhi1)
            croList.append(clusterPhi1)
        else:
            croFitness.append(fitnessPhi2)
            croList.append(clusterPhi2)

        # intermolecularSynthesis
        cluster2 = cro.intermolecularSynthesis(len(dataSet), k)
        croFitness.append(kmeans.fitnessCosWithDist(dataSet, cluster2, centroid, k))
        croList.append(cluster2)

        if fitness < max(croFitness):
            fitness = max(croFitness)
            newCluster = croList[croFitness.index(max(croFitness))]
            changedFitness = True

        if countIterCRO == 50:
            if changedFitness:
                f.write('Fitness CRO: ' + str(fitness) + '\n')
            else:
                f.write('k-means посчитал лучшее решение\n')
            break

    f.write('\n')
    h += 1
f.close()
