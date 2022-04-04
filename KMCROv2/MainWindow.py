from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.nameLbl = QtWidgets.QLabel(self.centralwidget)
        self.nameLbl.setGeometry(QtCore.QRect(10, 5, 110, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.nameLbl.setFont(font)
        self.nameLbl.setObjectName("nameLbl")
        self.fileNameLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.fileNameLineEdit.setGeometry(QtCore.QRect(160, 5, 460, 30))
        self.fileNameLineEdit.setObjectName("fileNameLineEdit")
        self.browserBtn = QtWidgets.QPushButton(self.centralwidget)
        self.browserBtn.setGeometry(QtCore.QRect(630, 5, 161, 30))
        self.browserBtn.setObjectName("browserBtn")
        self.euclidDistRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.euclidDistRadio.setGeometry(QtCore.QRect(160, 50, 141, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.euclidDistRadio.setFont(font)
        self.euclidDistRadio.setObjectName("euclidDistRadio")
        self.euclidDistRadio.setChecked(True)
        self.kMeansLbl = QtWidgets.QLabel(self.centralwidget)
        self.kMeansLbl.setGeometry(QtCore.QRect(10, 43, 110, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.kMeansLbl.setFont(font)
        self.kMeansLbl.setObjectName("kMeansLbl")
        self.cosineSimRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.cosineSimRadio.setGeometry(QtCore.QRect(300, 50, 141, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cosineSimRadio.setFont(font)
        self.cosineSimRadio.setObjectName("cosineSimRadio")
        self.outputEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.outputEdit.setGeometry(QtCore.QRect(10, 80, 781, 321))
        self.outputEdit.setObjectName("outputEdit")
        self.performBtn = QtWidgets.QPushButton(self.centralwidget)
        self.performBtn.setGeometry(QtCore.QRect(10, 410, 161, 30))
        self.performBtn.setObjectName("performBtn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "KMCRO"))
        self.nameLbl.setText(_translate("MainWindow", "Название файла"))
        self.browserBtn.setText(_translate("MainWindow", "Обзор"))
        self.euclidDistRadio.setText(_translate("MainWindow", "Euclidean Distance"))
        self.kMeansLbl.setText(_translate("MainWindow", "K-means"))
        self.cosineSimRadio.setText(_translate("MainWindow", "Cosine Similarity"))
        self.performBtn.setText(_translate("MainWindow", "Посчитать"))


