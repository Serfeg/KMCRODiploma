import random as r


def singleMoleculeCollision(lenDataSet, kNumber):
    phi = [r.randint(1, kNumber) for _ in range(lenDataSet)]
    newPhi = [i for i in phi]
    newPhi[r.randint(0, len(newPhi)-1)] = r.randint(1, kNumber)
    ### Здесь должна быть функция проверки пригодности данного "раствора", но пока что её нет
    return phi, newPhi


def singleMoleculeDecomposition(lenDataSet):
    pass


def intermolecularCollision(lenDataSet):
    pass


def intermolecularSynthesis(lenDataSet):
    pass


k = 3
n = 10
cluster, cluster1 = singleMoleculeCollision(n, k)
print(f"{cluster}\n{cluster1}")