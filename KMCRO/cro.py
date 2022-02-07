import random as r


def swap(x, y):
    tmp = x
    x = y
    y = tmp
    return x, y


def singleMoleculeCollision(lenDataSet, kNumber):
    originalPhi = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    newPhi = [i for i in originalPhi]
    newPhi[r.randint(0, lenDataSet-1)] = r.randint(1, kNumber)
    ### Здесь должна быть функция проверки пригодности данного "раствора", но пока что её нет
    return originalPhi, newPhi


def singleMoleculeDecomposition(lenDataSet, kNumber):
    originalPhi = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    oddPhi = [i for i in originalPhi]
    evenPhi = [i for i in originalPhi]
    for i in range(lenDataSet):
        if i % 2 == 0:
            evenPhi[i] = r.randint(1, kNumber)
        else:
            oddPhi[i] = r.randint(1, kNumber)
    ### Здесь должна быть функция проверки пригодности данного "раствора", но пока что её нет
    return originalPhi, oddPhi, evenPhi


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
    ### Здесь должна быть функция проверки пригодности данного "раствора", но пока что её нет
    return originalPhi1, newPhi1, originalPhi2, newPhi2


def intermolecularSynthesis(lenDataSet, kNumber):
    originalPhi1 = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    originalPhi2 = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    newPhi = []
    x = r.randint(0, lenDataSet-1)
    print(x)
    for i in range(lenDataSet):
        if i <= x:
            newPhi.append(originalPhi1[i])
        else:
            newPhi.append(originalPhi2[i])
    ### Здесь должна быть функция проверки пригодности данного "раствора", но пока что её нет
    return originalPhi1, originalPhi2, newPhi


k = 3
n = 10

cluster, cluster1, cluster2, cluster3 = intermolecularCollision(n, k)
print(f"{x},{y}\n{cluster}\n{cluster1}\n{cluster2}\n{cluster3}")
