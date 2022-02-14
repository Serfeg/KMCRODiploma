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
    return sumInUp / (m.sqrt(firstSumInDown) * m.sqrt(secondSumInDown)) if (m.sqrt(firstSumInDown) * m.sqrt(secondSumInDown)) != 0 else 0


def countSseCos(cosSim):
    sum = 0
    for i in range(len(cosSim)):
        sum += min(cosSim[i])
    return sum


def kMeansWithCos(dataSet, cluster, kNumber):
    exits = True
    k = 1
    while exits:
        centroid = [[findCentroid(dataSet, col, cluster, i + 1) for col in range(len(dataSet[0]))] for i in
                        range(kNumber)]
        cosSim = [[cosineSimilarity(dataSet[j], centroid[i]) for i in range(len(centroid))] for j in
                          range(len(dataSet))]
        newCluster = [cosSim[i].index(max(cosSim[i])) + 1 for i in range(len(cosSim))]
        if cluster == newCluster:
            exits = False
        else:
            cluster = newCluster
            k += 1
    sse = countSseCos(cosSim)
    return newCluster, centroid, sse, k


def kMeansFitness(dataSet, centroid):
    euclidDist = [[euclideanDistance(dataSet[j], centroid[i]) for i in range(len(centroid))] for j in
                      range(len(dataSet))]
    sse = countSse(euclidDist)
    return sse