import random as r


def swap(x, y):
    tmp = x
    x = y
    y = tmp
    return x, y


# Первый метод
def singleMoleculeCollision(lenDataSet, kNumber):
    originalPhi = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    newPhi = [i for i in originalPhi]
    newPhi[r.randint(0, lenDataSet - 1)] = r.randint(1, kNumber)
    return newPhi


# Второй метод
def singleMoleculeDecomposition(lenDataSet, kNumber):
    originalPhi = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    newPhi1 = [i for i in originalPhi]
    newPhi2 = [i for i in originalPhi]
    for i in range(lenDataSet):
        if i % 2 == 0:
            newPhi2[i] = r.randint(1, kNumber)
        else:
            newPhi1[i] = r.randint(1, kNumber)
    return newPhi1, newPhi2


# Третий метод
def intermolecularCollision(lenDataSet, kNumber):
    originalPhi1 = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    originalPhi2 = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    newPhi1 = [i for i in originalPhi2]
    newPhi2 = [i for i in originalPhi1]
    x = 0
    y = 0
    while x == y:
        x = r.randint(0, lenDataSet - 1)
        y = r.randint(0, lenDataSet - 1)
    if x > y:
        x, y = swap(x, y)
    for i in range(x, y+1):
        newPhi1[i] = originalPhi1[i]
        newPhi2[i] = originalPhi2[i]
    return newPhi1, newPhi2


# Четвёртый метод
def intermolecularSynthesis(lenDataSet, kNumber):
    originalPhi1 = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    originalPhi2 = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    newPhi = []
    x = r.randint(0, lenDataSet - 1)
    for i in range(lenDataSet):
        if i <= x:
            newPhi.append(originalPhi1[i])
        else:
            newPhi.append(originalPhi2[i])
    return newPhi



