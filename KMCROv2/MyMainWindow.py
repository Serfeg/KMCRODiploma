from MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow
import random as r
import kmeans
import math as m
import pandas as pd


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.clusterFile = ''
        self.typeKmeans = 'EuclidDist'
        self.browserBtn.clicked.connect(self.browseFile)
        self.euclidDistRadio.toggled.connect(self.checkMethodKMeans)
        self.cosineSimRadio.toggled.connect(self.checkMethodKMeans)
        self.performBtn.clicked.connect(self.performKmeans)

    def browseFile(self):
        fileName = QFileDialog.getOpenFileNames(None, 'Open File', './')[0]
        if fileName:
            self.clusterFile = fileName[0]
            self.fileNameLineEdit.setText(fileName[0])

    def checkMethodKMeans(self):
        if self.euclidDistRadio.isChecked():
            self.typeKmeans = 'EuclidDist'
        elif self.cosineSimRadio.isChecked():
            self.typeKmeans = 'CosSim'

    def performKmeans(self):
        if self.clusterFile != '':
            dataSet, eps = makeDataSet(self.clusterFile)
            # for i in range(len(dataSet)):
            #     sum = 0
            #     for j in range(len(dataSet[i])):
            #         sum += dataSet[i][j] ** 2
            #     sum = m.sqrt(sum)
            #     for j in range(len(dataSet[i])):
            #         dataSet[i][j] *= 1 / sum
            k = 4
            originalCluster = [r.randint(1, k) for i in range(len(dataSet))]

            if self.typeKmeans == 'EuclidDist':
                newCluster, centroid, sse, countIterKMeans = kmeans.kMeans(dataSet, originalCluster, k)
            elif self.typeKmeans == 'CosSim':
                newCluster, centroid, sse, countIterKMeans = kmeans.kMeansWithCos(dataSet, originalCluster, k)
            text = f"Count of Cluster: {k}\nSSE: {sse}\nCount of Iteration K-means: {countIterKMeans}\n"
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


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())