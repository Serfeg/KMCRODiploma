import math as m
import random as r
import kmeans
import cro

dataSet = [
    [5, 0],
    [5, 2],
    [3, 1],
    [0, 4],
    [2, 1],
    [4, 2],
    [2, 2],
    [2, 3],
    [1, 3],
    [5, 4]
]
originalCluster = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]

k = 2

f = open('text.txt', 'w')

f.write('Исходный датасет\n')
for i in range(len(dataSet)):
    for j in range(len(dataSet[i])):
        f.write(str(dataSet[i][j]) + "\t")
    f.write("\n")

f.write('\nНачальные кластера\n')
for i in range(len(originalCluster)):
    f.write(str(originalCluster[i]) + "\t")

f.write('\n\n')

sse = 0
h = 0
f.write('Cos+dist\n')
while h < 5:
    f.write('Итерация №' + str(h + 1) + '\n')
    f.write('Начальные центроиды\n')
    centroid = [[r.randint(-10, 10) for j in range(len(dataSet[0]))] for i in range(k)]
    for i in range(len(centroid)):
        f.write('C' + str(i + 1) + '\t')
        for j in range(len(centroid[i])):
            f.write(str(centroid[i][j]) + '\t')
        f.write('\n')
    f.write('\n')

    while True:
        cosSim = [[kmeans.cosineSimilarity(dataSet[j], centroid[i]) for i in range(len(centroid))] for j in
                  range(len(dataSet))]
        newCluster = [cosSim[i].index(max(cosSim[i])) + 1 for i in range(len(cosSim))]

        if originalCluster == newCluster:
            sse = kmeans.countSseCos(cosSim)
            break
        else:
            originalCluster = newCluster
            centroid = [[kmeans.findCentroid(dataSet, col, originalCluster, i + 1) for col in range(len(dataSet[0]))]
                        for i in
                        range(k)]

    f.write('Итоговые центроиды\n')
    for i in range(len(centroid)):
        f.write('C' + str(i + 1) + '\t')
        for j in range(len(centroid[i])):
            f.write(str(centroid[i][j]) + '\t')
        f.write('\n')
    f.write('\n')

    f.write('SSE: ' + str(sse) + '\n\n')
    fitness = kmeans.fitnessCosWithDist(dataSet, originalCluster, centroid, k)
    f.write('Fitness: ' + str(fitness) + '\n')
    countIterCRO = 0
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

        if countIterCRO == 100:
            f.write('singleMoleculeCollision fitness: ' + str(croFitness[0]) + '\n')
            f.write('singleMoleculeDecomposition fitness: ' + str(croFitness[1]) + '\n')
            f.write('intermolecularCollision fitness: ' + str(croFitness[2]) + '\n')
            f.write('intermolecularSynthesis fitness: ' + str(croFitness[3]) + '\n')
            break

    f.write('\n')
    h += 1
f.close()
