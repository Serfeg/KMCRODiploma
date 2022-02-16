import math as m


# Расчёт центроид
def findCentroid(dataSet, dataSetColumn, cluster, kNumber):
    sum = 0
    z = 0
    for i in range(len(dataSet)):
        if cluster[i] == kNumber:
            z += 1
            sum += dataSet[i][dataSetColumn]
    return round(sum / z, 2) if z != 0 else 0


# Расчёт евклидова расстояния
def euclideanDistance(dataSetRow, centroid):
    sum = 0
    for i in range(len(dataSetRow)):
        sum += (dataSetRow[i] - centroid[i]) ** 2
    return sum


# Расчёт квадратичной ошибки
def countSse(euclidDist):
    sum = 0
    for i in range(len(euclidDist)):
        sum += min(euclidDist[i])
    return sum


def kMeans(dataSet, cluster, kNumber):
    exits = True
    k = 1
    while exits:
        centroid = [[findCentroid(dataSet, col, cluster, i + 1) for col in range(len(dataSet[0]))] for i in
                    range(kNumber)]
        euclidDist = [[euclideanDistance(dataSet[j], centroid[i]) for i in range(len(centroid))] for j in
                      range(len(dataSet))]
        newCluster = [euclidDist[i].index(min(euclidDist[i])) + 1 for i in range(len(euclidDist))]
        if cluster == newCluster:
            exits = False
        else:
            cluster = newCluster
            k += 1
    sse = countSse(euclidDist)
    return cluster, centroid, sse, k


def cosineSimilarity(dataSetRow, centroid):
    sumInUp = 0
    firstSumInDown = 0
    secondSumInDown = 0
    for i in range(len(dataSetRow)):
        sumInUp += dataSetRow[i] * centroid[i]
        firstSumInDown += dataSetRow[i] ** 2
        secondSumInDown += centroid[i] ** 2
    sumInDown = (m.sqrt(firstSumInDown) * m.sqrt(secondSumInDown))
    return sumInUp / sumInDown if sumInDown != 0 else 0


def countSseCos(cosSim):
    sum = 0
    for i in range(len(cosSim)):
        sum += max(cosSim[i])
    return sum


def kMeansWithCos(dataSet, cluster, kNumber):
    exits = True
    k = 0
    while exits:
        k += 1
        centroid = [[findCentroid(dataSet, col, cluster, i + 1) for col in range(len(dataSet[0]))] for i in
                        range(kNumber)]
        cosSim = [[cosineSimilarity(dataSet[j], centroid[i]) for i in range(len(centroid))] for j in
                          range(len(dataSet))]
        newCluster = [cosSim[i].index(max(cosSim[i])) + 1 for i in range(len(cosSim))]
        if cluster == newCluster:
            exits = False
        else:
            cluster = newCluster
    sse = countSseCos(cosSim)
    return newCluster, centroid, sse, k


def distance(dataSetRow, centroid):
    sum = 0
    for i in range(len(dataSetRow)):
        sum += abs(dataSetRow[i] - centroid[i])
    return m.sqrt(sum)


def obj(dataSetRow, centroid):
    return cosineSimilarity(dataSetRow, centroid) + (1 - distance(dataSetRow, centroid))


def fitnessCosWithDist(dataSet, cluster, centroid, nK):
    sumObj = 0
    sumInUp = 0
    for i in range(len(nK)):
        for j in range(len(dataSet)):
            if cluster[j] == i+1:
                sumObj += obj(dataSet[j], centroid[i])
        sumInUp += sumObj / nK[i]
    return sumInUp / len(nK)
