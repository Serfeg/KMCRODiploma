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


def kMeans(dataSet, cluster, lenDataSet, kNumber):
    exits = True
    k = 1
    while exits:
        centroid = [[findCentroid(dataSet, col, cluster, i + 1) for col in range(len(dataSet[0]))] for i in range(kNumber)]
        euclidDist = [[euclideanDistance(dataSet[j], centroid[i]) for i in range(len(centroid))] for j in
                      range(lenDataSet)]
        newCluster = [euclidDist[i].index(min(euclidDist[i])) + 1 for i in range(len(euclidDist))]
        sse = countSse(euclidDist)
        if cluster == newCluster:
            exits = False
        else:
            cluster = newCluster
            k += 1
    return cluster, centroid, sse, k
