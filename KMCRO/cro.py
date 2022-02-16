import random as r


def swap(x, y):
    tmp = x
    x = y
    y = tmp
    return x, y


# Первый метод, индекс 0
def singleMoleculeCollision(lenDataSet, kNumber):
    originalPhi = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    newPhi = [i for i in originalPhi]
    newPhi[r.randint(0, lenDataSet-1)] = r.randint(1, kNumber)
    return newPhi


# Второй метод, индекс 1
def singleMoleculeDecomposition(lenDataSet, kNumber):
    originalPhi = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    oddPhi = [i for i in originalPhi]
    evenPhi = [i for i in originalPhi]
    for i in range(lenDataSet):
        if i % 2 == 0:
            evenPhi[i] = r.randint(1, kNumber)
        else:
            oddPhi[i] = r.randint(1, kNumber)
    return oddPhi, evenPhi


# Третий метод, индекс 2
def intermolecularCollision(lenDataSet, kNumber):
    originalPhi1 = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    originalPhi2 = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    newPhi1 = [i for i in originalPhi1]
    newPhi2 = [i for i in originalPhi2]
    x = 0
    y = 0
    while x == y:
        x = r.randint(0, lenDataSet - 1)
        y = r.randint(0, lenDataSet - 1)
    if x > y:
        x, y = swap(x, y)
    for i in range(x, y):
        newPhi1[i] = r.randint(1, kNumber)
        newPhi2[i] = r.randint(1, kNumber)
    return newPhi1, newPhi2


# Четвёртый метод, индекс 3
def intermolecularSynthesis(lenDataSet, kNumber):
    originalPhi1 = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    originalPhi2 = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    newPhi = []
    x = r.randint(0, lenDataSet-1)
    for i in range(lenDataSet):
        if i <= x:
            newPhi.append(originalPhi1[i])
        else:
            newPhi.append(originalPhi2[i])
    return newPhi
