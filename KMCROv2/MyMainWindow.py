from MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow
import random as r
import kmeans
import math as m
import cro
import pandas as pd


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.clusterFile = ''
        self.countCluster = 2
        self.typeKmeans = 'EuclidDist'
        self.countIterCRO = 0
        self.useCRO = False
        self.useNormalization = False
        self.browserBtn.clicked.connect(self.browseFile)
        self.countClusterSBox.valueChanged.connect(self.countClusterResult)
        self.countIterCroSBox.valueChanged.connect(self.countIterCroResult)
        self.croCheckBox.toggled.connect(self.checkCRO)
        self.normalizationCheckBox.toggled.connect(self.checkNormalization)
        self.euclidDistRadio.toggled.connect(self.checkMethodKMeans)
        self.cosineSimRadio.toggled.connect(self.checkMethodKMeans)
        self.cosEuclidRadio.toggled.connect(self.checkMethodKMeans)
        self.performBtn.clicked.connect(self.performKmeans)

    def browseFile(self):
        fileName = QFileDialog.getOpenFileNames(self, 'Open File', './')[0]
        if fileName:
            self.clusterFile = fileName[0]
            self.fileNameLineEdit.setText(fileName[0])

    def checkMethodKMeans(self):
        if self.euclidDistRadio.isChecked():
            self.typeKmeans = 'EuclidDist'
        elif self.cosineSimRadio.isChecked():
            self.typeKmeans = 'CosSim'
        elif self.cosEuclidRadio.isChecked():
            self.typeKmeans = 'CosEuclid'

    def countClusterResult(self):
        self.countCluster = self.countClusterSBox.value()

    def countIterCroResult(self):
        self.countIterCRO = self.countIterCroSBox.value()

    def checkCRO(self):
        if self.croCheckBox.isChecked():
            self.countIterCroSBox.setEnabled(True)
            self.useCRO = True
        else:
            self.countIterCroSBox.setEnabled(False)
            self.useCRO = False

    def checkNormalization(self):
        if self.normalizationCheckBox.isChecked():
            self.useNormalization = True
        else:
            self.useNormalization = False

    def performKmeans(self):
        if self.clusterFile != '':
            dataSet, eps = makeDataSet(self.clusterFile)
            if self.useNormalization:
                makeNormalization(dataSet)

            k = self.countCluster
            originalCluster = [r.randint(1, k) for i in range(len(dataSet))]

            if self.typeKmeans == 'EuclidDist':
                newCluster, centroid, sse, countIterKMeans = kmeans.kMeans(dataSet, originalCluster, k)
                fitness = kmeans.fitnessEuclidDist(dataSet, newCluster, centroid, k)
            elif self.typeKmeans == 'CosSim':
                newCluster, centroid, sse, countIterKMeans = kmeans.kMeansWithCos(dataSet, originalCluster, k)
                fitness = kmeans.fitnessCos(dataSet, newCluster, centroid, k)
            elif self.typeKmeans == 'CosEuclid':
                newCluster, centroid, sse, countIterKMeans = kmeans.kMeansWithCosAndEuclid(dataSet, originalCluster, k)
                fitness = kmeans.fitnessCosWithDist(dataSet, newCluster, centroid, k)
            text = f"Type K-means: {self.typeKmeans}\nCount of Cluster: {k}\nSSE: {sse}\nCount of Iteration K-means: {countIterKMeans}\nFitness: {fitness}"
            self.outputEdit.setText(text)
        else:
            self.outputEdit.setText('Выберите файл')


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


def makeNormalization(dataSet):
    for i in range(len(dataSet)):
        sum = 0
        for j in range(len(dataSet[i])):
            sum += dataSet[i][j] ** 2
        sum = m.sqrt(sum)
        for j in range(len(dataSet[i])):
            dataSet[i][j] *= 1 / sum
    return dataSet


def makeFitness(dataSet, k, centroid, iterCRO, fitness, typeKMeans):
    countIterCRO = 0
    newFitness = fitness
    newCluster = []
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


        if typeKMeans == 'EuclidDist':
            if newFitness > min(croFitness):
                newFitness = min(croFitness)
                newCluster = croList[croFitness.index(min(croFitness))]
        else:
            if newFitness < max(croFitness):
                newFitness = max(croFitness)
                newCluster = croList[croFitness.index(max(croFitness))]

        if countIterCRO == iterCRO:
            break

    return newFitness, newCluster


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())