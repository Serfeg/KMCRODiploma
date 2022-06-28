import os

from MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow
import random as r
import kmeans
import math as m
import cro
import pandas as pd
import statistics
import matplotlib.pyplot as plt


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.clusterFile = ''
        self.countCluster = 2
        self.typeKmeans = 'EuclidDist'
        self.countIterCRO = 0
        self.countIterAnalysis = 0
        self.useCRO = False
        self.useNormalization = False
        self.browserBtn.clicked.connect(self.browseFile)
        self.countClusterSBox.valueChanged.connect(self.countClusterResult)
        self.countIterCroSBox.valueChanged.connect(self.countIterCroResult)
        self.countIterSBox.valueChanged.connect(self.countIterAnalysisResult)
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

    def countIterAnalysisResult(self):
        self.countIterAnalysis = self.countIterSBox.value()

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
            originalCluster = [r.randint(1, k) for _ in range(len(dataSet))]

            #makeAnalysis(dataSet, k, self.countIterAnalysis, self.countIterCRO)
            if self.typeKmeans == 'EuclidDist':
                newCluster, centroid, sse, countIterKMeans = kmeans.kMeans(dataSet, originalCluster, k)
                fitness = kmeans.fitnessEuclidDist(dataSet, newCluster, centroid, k)
                makeNewAnalysis(dataSet, k, self.countIterCRO, self.countIterAnalysis, 'tests', self.typeKmeans)
            elif self.typeKmeans == 'CosSim':
                newCluster, centroid, sse, countIterKMeans = kmeans.kMeansWithCos(dataSet, originalCluster, k)
                fitness = kmeans.fitnessCos(dataSet, newCluster, centroid, k)
                makeNewAnalysis(dataSet, k, self.countIterCRO, self.countIterAnalysis, 'tests', self.typeKmeans)
            elif self.typeKmeans == 'CosEuclid':
                newCluster, centroid, sse, countIterKMeans = kmeans.kMeansWithCosAndEuclid(dataSet, originalCluster, k)
                fitness = kmeans.fitnessCosWithDist(dataSet, newCluster, centroid, k)
                makeNewAnalysis(dataSet, k, self.countIterCRO, self.countIterAnalysis, 'tests', self.typeKmeans)
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


def makeFitnessEuclidDist(dataSet, k, centroid, iterCRO):
    newFitness = 10000
    newCluster = []

    for i in range(iterCRO):
        croFitness = []
        croList = []

        # singleMoleculeCollision
        cluster1 = cro.singleMoleculeCollision(len(dataSet), k)
        croFitness.append(kmeans.fitnessEuclidDist(dataSet, cluster1, centroid, k))
        croList.append(cluster1)

        # singleMoleculeDecomposition
        clusterOdd, clusterEven = cro.singleMoleculeDecomposition(len(dataSet), k)
        fitnessOdd = kmeans.fitnessEuclidDist(dataSet, clusterOdd, centroid, k)
        fitnessEven = kmeans.fitnessEuclidDist(dataSet, clusterEven, centroid, k)
        if fitnessOdd >= fitnessEven:
            croFitness.append(fitnessOdd)
            croList.append(clusterOdd)
        else:
            croFitness.append(fitnessEven)
            croList.append(clusterEven)

        # intermolecularCollision
        clusterPhi1, clusterPhi2 = cro.intermolecularCollision(len(dataSet), k)
        fitnessPhi1 = kmeans.fitnessEuclidDist(dataSet, clusterPhi1, centroid, k)
        fitnessPhi2 = kmeans.fitnessEuclidDist(dataSet, clusterPhi2, centroid, k)
        if fitnessPhi1 >= fitnessPhi2:
            croFitness.append(fitnessPhi1)
            croList.append(clusterPhi1)
        else:
            croFitness.append(fitnessPhi2)
            croList.append(clusterPhi2)

        # intermolecularSynthesis
        cluster2 = cro.intermolecularSynthesis(len(dataSet), k)
        croFitness.append(kmeans.fitnessEuclidDist(dataSet, cluster2, centroid, k))
        croList.append(cluster2)

        if newFitness > min(croFitness):
            newFitness = min(croFitness)
            newCluster = croList[croFitness.index(min(croFitness))]

    return newFitness, newCluster


def makeFitnessCos(dataSet, k, centroid, iterCRO):
    newFitness = -10000
    newCluster = []

    for i in range(iterCRO):
        croFitness = []
        croList = []

        # singleMoleculeCollision
        cluster1 = cro.singleMoleculeCollision(len(dataSet), k)
        croFitness.append(kmeans.fitnessCos(dataSet, cluster1, centroid, k))
        croList.append(cluster1)

        # singleMoleculeDecomposition
        clusterOdd, clusterEven = cro.singleMoleculeDecomposition(len(dataSet), k)
        fitnessOdd = kmeans.fitnessCos(dataSet, clusterOdd, centroid, k)
        fitnessEven = kmeans.fitnessCos(dataSet, clusterEven, centroid, k)
        if fitnessOdd >= fitnessEven:
            croFitness.append(fitnessOdd)
            croList.append(clusterOdd)
        else:
            croFitness.append(fitnessEven)
            croList.append(clusterEven)

        # intermolecularCollision
        clusterPhi1, clusterPhi2 = cro.intermolecularCollision(len(dataSet), k)
        fitnessPhi1 = kmeans.fitnessCos(dataSet, clusterPhi1, centroid, k)
        fitnessPhi2 = kmeans.fitnessCos(dataSet, clusterPhi2, centroid, k)
        if fitnessPhi1 >= fitnessPhi2:
            croFitness.append(fitnessPhi1)
            croList.append(clusterPhi1)
        else:
            croFitness.append(fitnessPhi2)
            croList.append(clusterPhi2)

        # intermolecularSynthesis
        cluster2 = cro.intermolecularSynthesis(len(dataSet), k)
        croFitness.append(kmeans.fitnessCos(dataSet, cluster2, centroid, k))
        croList.append(cluster2)

        if newFitness < max(croFitness):
            newFitness = max(croFitness)
            newCluster = croList[croFitness.index(max(croFitness))]

    return newFitness, newCluster


def makeFitnessCosAndEuclid(dataSet, k, centroid, iterCRO):
    newFitness = -10000
    newCluster = []

    for i in range(iterCRO):
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

        if newFitness < max(croFitness):
            newFitness = max(croFitness)
            newCluster = croList[croFitness.index(max(croFitness))]

    return newFitness, newCluster


def makeAnalysis(dataSet, k, countIterAnalysis, iterCRO):
    epochs = 0
    kMeans = []
    CRO = []
    file = open('text.txt', 'w')
    file.write('Euclidean Distance\n')
    file.write('Iteration\tSSE\tFitness\n')
    while epochs < countIterAnalysis:
        epochs += 1
        originalCluster = [r.randint(1, k) for _ in range(len(dataSet))]
        newCluster, centroid, sse, countIterKMeans = kmeans.kMeans(dataSet, originalCluster, k)
        #fitness = kmeans.fitnessEuclidDist(dataSet, newCluster, centroid, k)
        newFitness, cluster = makeFitnessEuclidDist(dataSet, k, centroid, iterCRO)
        kMeans.append(sse)
        CRO.append(newFitness)
        file.write(str(epochs)+"\t"+str(sse)+"\t"+str(newFitness)+"\n")
        file.write("\tКластера\n")
        for i in range(len(newCluster)):
            file.write("\t\tСтрока "+str(i+1)+"\t"+str(newCluster[i]-1)+"\n")

    file.write("Min" + " " + str(min(kMeans)) + " " + str(min(CRO)) + "\n")
    file.write("Max" + " " + str(max(kMeans)) + " " + str(max(CRO)) + "\n")
    file.write("Mean" + " " + str(statistics.mean(kMeans)) + " " + str(statistics.mean(CRO)) + "\n")
    file.write("Standard deviation" + " " + str(statistics.pstdev(kMeans)) + " " + str(statistics.pstdev(CRO)) + "\n")
    file.write("Coefficient of variation" + " " + str((statistics.pstdev(kMeans) / statistics.mean(kMeans)) * 100) + " " +
                      str((statistics.pstdev(CRO) / statistics.mean(CRO)) * 100) + "\n")
    file.write("Span Factor" + " " + str(max(kMeans) - min(kMeans)) + " " + str(max(CRO) - min(CRO)) + "\n")

    epochs = 0
    kMeans = []
    CRO = []

    file.write('Cosine Similarity\n')
    file.write('Iteration\tSSE\tFitness\n')
    while epochs < countIterAnalysis:
        epochs += 1
        originalCluster = [r.randint(1, k) for _ in range(len(dataSet))]
        newCluster, centroid, sse, countIterKMeans = kmeans.kMeansWithCos(dataSet, originalCluster, k)
        #fitness = kmeans.fitnessCos(dataSet, newCluster, centroid, k)
        kMeans.append(sse)
        newFitness, cluster = makeFitnessCos(dataSet, k, centroid, iterCRO)
        CRO.append(newFitness)
        file.write(str(epochs) + "\t" + str(sse) + "\t" + str(newFitness) + "\n")
        file.write("\tКластера\n")
        for i in range(len(newCluster)):
            file.write("\t\tСтрока " + str(i + 1) + "\t" + str(newCluster[i] - 1) + "\n")

    file.write("Min" + " " + str(min(kMeans)) + " " + str(min(CRO)) + "\n")
    file.write("Max" + " " + str(max(kMeans)) + " " + str(max(CRO)) + "\n")
    file.write("Mean" + " " + str(statistics.mean(kMeans)) + " " + str(statistics.mean(CRO))+ "\n")
    file.write("Standard deviation" + " " + str(statistics.pstdev(kMeans)) + " " + str(statistics.pstdev(CRO))+ "\n")
    file.write(
        "Coefficient of variation" + " " + str((statistics.pstdev(kMeans) / statistics.mean(kMeans)) * 100) + " " +
        str((statistics.pstdev(CRO) / statistics.mean(CRO)) * 100) + "\n")
    file.write("Span Factor" + " " + str(max(kMeans) - min(kMeans)) + " " + str(max(CRO) - min(CRO)) + "\n")

    epochs = 0
    kMeans = []
    CRO = []
    file.write('Cosine Similarity + Euclidean Distance\n')
    file.write('Iteration\tSSE\tFitness\n')
    while epochs < countIterAnalysis:
        epochs += 1
        originalCluster = [r.randint(1, k) for _ in range(len(dataSet))]
        newCluster, centroid, sse, countIterKMeans = kmeans.kMeansWithCosAndEuclid(dataSet, originalCluster, k)
        #fitness = kmeans.fitnessCosWithDist(dataSet, newCluster, centroid, k)
        kMeans.append(sse)
        newFitness, cluster = makeFitnessCosAndEuclid(dataSet, k, centroid, iterCRO)
        CRO.append(newFitness)
        file.write(str(epochs) + "\t" + str(sse) + "\t" + str(newFitness) + "\n")
        file.write("\tКластера\n")
        for i in range(len(newCluster)):
            file.write("\t\tСтрока " + str(i + 1) + "\t" + str(newCluster[i] - 1) + "\n")

    file.write("Min" + " " + str(min(kMeans)) + " " + str(min(CRO)) + "\n")
    file.write("Max" + " " + str(max(kMeans)) + " " + str(max(CRO)) + "\n")
    file.write("Mean" + " " + str(statistics.mean(kMeans)) + " " + str(statistics.mean(CRO)) + "\n")
    file.write("Standard deviation" + " " + str(statistics.pstdev(kMeans)) + " " + str(statistics.pstdev(CRO)) + "\n")
    file.write("Coefficient of variation" + " " + str((statistics.pstdev(kMeans) / statistics.mean(kMeans)) * 100) + " " +
                      str((statistics.pstdev(CRO) / statistics.mean(CRO)) * 100) + "\n")
    file.write("Span Factor" + " " + str(max(kMeans) - min(kMeans)) + " " + str(max(CRO) - min(CRO)) + "\n")

    file.close()
    #print(df)
    # x = ['Euclidean Distance', 'Cosine Similarity', 'Cos + Euclid']
    # print(histKMeansVariationList)
    # colors = ['red', 'green', 'blue']
    # #plt.hist(histKMeansDeviationList, color='red', edgecolor='black')
    # fig, ax = plt.subplots()
    #
    # ax.bar(x, histKMeansVariationList)
    #
    # ax.set_facecolor('seashell')
    # fig.set_facecolor('floralwhite')
    #
    # plt.title('Histogram of Standard deviation')
    # plt.show()


def makeNewAnalysis(dataSet, k, iterCRO, countIterAnalysis, path, typeKMeans):
    os.chdir(path)
    kMeans = []
    CRO = []
    if typeKMeans == 'EuclidDist':
        for i in range(countIterAnalysis):
            file = open('Запуск '+str(i+1)+' kmeans'+'.txt', 'w+')
            originalCluster = [r.randint(1, k) for _ in range(len(dataSet))]
            newClusterKmeans, centroid, sse, countIterKMeans = kmeans.kMeans(dataSet, originalCluster, k)
            fitness = kmeans.fitnessEuclidDist(dataSet, newClusterKmeans, centroid, k)
            for j in range(len(newClusterKmeans)):
                file.write("Строка " + str(j + 1) + "\t" + str(newClusterKmeans[j] - 1) + "\n")
            file.write("Количество итераций KMeans:\t" + str(countIterKMeans) + "\n")
            file.write("SSE:\t"+str(sse)+"\n")
            file.write("Fitness\t"+str(fitness))
            file.close()
            kMeans.append(sse)
            fileCRO = open('Запуск '+str(i+1)+' kmeans+CRO'+'.txt', 'w+')
            newFitness, fitnessCluster = makeFitnessEuclidDist(dataSet, k, centroid, iterCRO)
            if newFitness > fitness:
                fileCRO.write('Лучшее решение было найдено Kmeans\n')
                for j in range(len(newClusterKmeans)):
                    fileCRO.write("Строка " + str(j + 1) + "\t" + str(newClusterKmeans[j] - 1) + "\n")
                fileCRO.write("Количество итераций KMeans:\t" + str(countIterKMeans) + "\n")
                fileCRO.write("SSE:\t" + str(sse) + "\n")
                fileCRO.write("Fitness\t" + str(fitness))
                CRO.append(fitness)
            else:
                fileCRO.write('Лучшее решение было найдено CRO\n')
                for j in range(len(fitnessCluster)):
                    fileCRO.write("Строка " + str(j + 1) + "\t" + str(fitnessCluster[j] - 1) + "\n")
                fileCRO.write("Количество итераций KMeans:\t" + str(countIterKMeans) + "\n")
                fileCRO.write("SSE:\t" + str(sse) + "\n")
                fileCRO.write("Fitness\t" + str(newFitness))
                CRO.append(newFitness)
            fileCRO.close()
        file = open('Общий_файл.txt', 'w+')
        file.write('Номер запуска\tSSE\tFitness\n')
        for i in range(countIterAnalysis):
            file.write('Запуск '+str(i+1)+'\t'+str(kMeans[i])+'\t'+str(CRO[i])+'\n')
        file.write("Min" + " " + str(min(kMeans)) + " " + str(min(CRO)) + "\n")
        file.write("Max" + " " + str(max(kMeans)) + " " + str(max(CRO)) + "\n")
        file.write("Mean" + " " + str(statistics.mean(kMeans)) + " " + str(statistics.mean(CRO)) + "\n")
        file.write("Standard deviation" + " " + str(statistics.pstdev(kMeans)) + " " + str(statistics.pstdev(CRO)) + "\n")
        file.write(
            "Coefficient of variation" + " " + str((statistics.pstdev(kMeans) / statistics.mean(kMeans)) * 100) + " " +
            str((statistics.pstdev(CRO) / statistics.mean(CRO)) * 100) + "\n")
        file.write("Span Factor" + " " + str(max(kMeans) - min(kMeans)) + " " + str(max(CRO) - min(CRO)) + "\n")
        file.close()
    elif typeKMeans == 'CosSim':
        for i in range(countIterAnalysis):
            file = open('Запуск '+str(i+1)+' kmeans'+'.txt', 'w+')
            originalCluster = [r.randint(1, k) for _ in range(len(dataSet))]
            newClusterKmeans, centroid, sse, countIterKMeans = kmeans.kMeansWithCos(dataSet, originalCluster, k)
            fitness = kmeans.fitnessCos(dataSet, newClusterKmeans, centroid, k)
            for j in range(len(newClusterKmeans)):
                file.write("Строка " + str(j + 1) + "\t" + str(newClusterKmeans[j] - 1) + "\n")
            file.write("Количество итераций KMeans:\t" + str(countIterKMeans) + "\n")
            file.write("SSE:\t"+str(sse)+"\n")
            file.write("Fitness\t"+str(fitness))
            file.close()
            kMeans.append(sse)
            fileCRO = open('Запуск '+str(i+1)+' kmeans+CRO'+'.txt', 'w+')
            newFitness, fitnessCluster = makeFitnessCos(dataSet, k, centroid, iterCRO)
            if fitness > newFitness:
                fileCRO.write('Лучшее решение было найдено Kmeans\n')
                for j in range(len(newClusterKmeans)):
                    fileCRO.write("Строка " + str(j + 1) + "\t" + str(newClusterKmeans[j] - 1) + "\n")
                fileCRO.write("Количество итераций KMeans:\t" + str(countIterKMeans) + "\n")
                fileCRO.write("SSE:\t" + str(sse) + "\n")
                fileCRO.write("Fitness\t" + str(fitness))
                CRO.append(fitness)
            else:
                fileCRO.write('Лучшее решение было найдено CRO\n')
                for j in range(len(fitnessCluster)):
                    fileCRO.write("Строка " + str(j + 1) + "\t" + str(fitnessCluster[j] - 1) + "\n")
                fileCRO.write("Количество итераций KMeans:\t" + str(countIterKMeans) + "\n")
                fileCRO.write("SSE:\t" + str(sse) + "\n")
                fileCRO.write("Fitness\t" + str(newFitness))
                CRO.append(newFitness)
            fileCRO.close()
        file = open('Общий_файл.txt', 'w+')
        file.write('Номер запуска\tSSE\tFitness\n')
        for i in range(countIterAnalysis):
            file.write('Запуск '+str(i+1)+'\t'+str(kMeans[i])+'\t'+str(CRO[i])+'\n')
        file.write("Min" + " " + str(min(kMeans)) + " " + str(min(CRO)) + "\n")
        file.write("Max" + " " + str(max(kMeans)) + " " + str(max(CRO)) + "\n")
        file.write("Mean" + " " + str(statistics.mean(kMeans)) + " " + str(statistics.mean(CRO)) + "\n")
        file.write("Standard deviation" + " " + str(statistics.pstdev(kMeans)) + " " + str(statistics.pstdev(CRO)) + "\n")
        file.write(
            "Coefficient of variation" + " " + str((statistics.pstdev(kMeans) / statistics.mean(kMeans)) * 100) + " " +
            str((statistics.pstdev(CRO) / statistics.mean(CRO)) * 100) + "\n")
        file.write("Span Factor" + " " + str(max(kMeans) - min(kMeans)) + " " + str(max(CRO) - min(CRO)) + "\n")
        file.close()
    elif typeKMeans == 'CosEuclid':
        for i in range(countIterAnalysis):
            file = open('Запуск '+str(i+1)+' kmeans'+'.txt', 'w+')
            originalCluster = [r.randint(1, k) for _ in range(len(dataSet))]
            newClusterKmeans, centroid, sse, countIterKMeans = kmeans.kMeansWithCosAndEuclid(dataSet, originalCluster, k)
            fitness = kmeans.fitnessCosWithDist(dataSet, newClusterKmeans, centroid, k)
            for j in range(len(newClusterKmeans)):
                file.write("Строка " + str(j + 1) + "\t" + str(newClusterKmeans[j] - 1) + "\n")
            file.write("Количество итераций KMeans:\t" + str(countIterKMeans) + "\n")
            file.write("SSE:\t"+str(sse)+"\n")
            file.write("Fitness\t"+str(fitness))
            file.close()
            kMeans.append(sse)
            fileCRO = open('Запуск '+str(i+1)+' kmeans+CRO'+'.txt', 'w+')
            newFitness, fitnessCluster = makeFitnessCosAndEuclid(dataSet, k, centroid, iterCRO)
            if fitness > newFitness:
                fileCRO.write('Лучшее решение было найдено Kmeans\n')
                for j in range(len(newClusterKmeans)):
                    fileCRO.write("Строка " + str(j + 1) + "\t" + str(newClusterKmeans[j] - 1) + "\n")
                fileCRO.write("Количество итераций KMeans:\t" + str(countIterKMeans) + "\n")
                fileCRO.write("SSE:\t" + str(sse) + "\n")
                fileCRO.write("Fitness\t" + str(fitness))
                CRO.append(fitness)
            else:
                fileCRO.write('Лучшее решение было найдено CRO\n')
                for j in range(len(fitnessCluster)):
                    fileCRO.write("Строка " + str(j + 1) + "\t" + str(fitnessCluster[j] - 1) + "\n")
                fileCRO.write("Количество итераций KMeans:\t" + str(countIterKMeans) + "\n")
                fileCRO.write("SSE:\t" + str(sse) + "\n")
                fileCRO.write("Fitness\t" + str(newFitness))
                CRO.append(newFitness)
            fileCRO.close()
        file = open('Общий_файл.txt', 'w+')
        file.write('Номер запуска\tSSE\tFitness\n')
        for i in range(countIterAnalysis):
            file.write('Запуск '+str(i+1)+'\t'+str(kMeans[i])+'\t'+str(CRO[i])+'\n')
        file.write("Min" + " " + str(min(kMeans)) + " " + str(min(CRO)) + "\n")
        file.write("Max" + " " + str(max(kMeans)) + " " + str(max(CRO)) + "\n")
        file.write("Mean" + " " + str(statistics.mean(kMeans)) + " " + str(statistics.mean(CRO)) + "\n")
        file.write("Standard deviation" + " " + str(statistics.pstdev(kMeans)) + " " + str(statistics.pstdev(CRO)) + "\n")
        file.write(
            "Coefficient of variation" + " " + str((statistics.pstdev(kMeans) / statistics.mean(kMeans)) * 100) + " " +
            str((statistics.pstdev(CRO) / statistics.mean(CRO)) * 100) + "\n")
        file.write("Span Factor" + " " + str(max(kMeans) - min(kMeans)) + " " + str(max(CRO) - min(CRO)) + "\n")
        file.close()
    os.chdir("..")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
