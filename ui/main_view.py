import sys
import threading
import time
import pandas
import numpy
import pyqtgraph

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from database.database_manager import DatabaseManager
from load_forecast.data_converter import DataConverter
from load_forecast.training.data_preparer import DataPreparer
from load_forecast.training.ann_regression import AnnRegression
from load_forecast.scorer import Scorer
from load_forecast.plotting import Plotting
from ui.service_invoker import ServiceInvoker
#from front.stream import Stream

class MainWindow(QMainWindow):
    file = None
    loaded_model_name = None
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("ui/frontend.ui", self)
        self.browseCSVButton.clicked.connect(self.browse_files)
        self.browseModelButton.clicked.connect(self.browse_model)
        self.saveButton.clicked.connect(self.write_to_database)
        #self.trainButton.clicked.connect(self.start_ann_thread)
        self.trainButton.clicked.connect(self.start_ann)
        self.loadModelButton.clicked.connect(self.load_model_for_prediction)

        self.file = None
        self.loaded_model_name = ''

        self.service_invoker = ServiceInvoker()


       # sys.stdout = Stream(newText=self.onUpdateText)

        #x = threading.Thread(target=self.listen)
        #x.start()

    # def write_to_database_thread(self):
    #     x = threading.Thread(target=self.write_to_database)
    #     x.start()

    # def start_ann_thread(self):
    #     x = threading.Thread(target=self.start_ann)
    #     x.start()

    def onUpdateText(self, text):
        cursor = self.textedit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textedit.setTextCursor(cursor)
        self.textedit.ensureCursorVisible()


    # def plot(self, graph, color, name):
    #     self.graphWidget.plot(graph, pen=pyqtgraph.mkPen(color, width=3), name=name)

    # def addLegend(self):
    #     self.graphWidget.addLegend()

    def browse_files(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open file', 'data', 'XLSX (*.xlsx)')
        self.importCSVEdit.setText(self.file[0].split('/')[-1])
        if self.file is not None:
            self.saveButton.setEnabled(True)
            self.loaded_model_name = None
            self.importModelEdit.setText('')

    def browse_model(self):
        #_OutputFolder = QFileDialog::getExistingDirectory(0, ("Select Output Folder"), QDir::currentPath());
        self.loaded_model_name = QFileDialog.getExistingDirectory(self, 'Select model', '')
        name = self.loaded_model_name.split('/')[-1]
        self.importModelEdit.setText(name)
        self.loaded_model_name = name
        if self.loaded_model_name is not None:
            self.loadModelButton.setEnabled(True)
            self.predictButton.setEnabled(True)
            self.file = None
            self.importCSVEdit.setText('')

    def write_to_database(self):
        if self.file is None:   # return if filename is not loaded
            return

        print("Loading and converting data...")
        importCSVEdit = "data/" + self.importCSVEdit.text()#.split('/')[-1]
        try:
            self.preprocessed_data, function_result = self.service_invoker.write_data_to_database(importCSVEdit)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
            return

        # once we write the data to the database, we can enable the button for training
        self.trainButton.setEnabled(True)
        QMessageBox.information(self, "Info", 'Preprocessed data saved to database!', QMessageBox.Ok)
        return function_result

    def start_ann(self):
        model_loaded = False
        if self.loaded_model_name is not None:
            model_loaded = True
        else:
            self.loaded_model_name = ''

        train_start = self.trainingFromDate.dateTime()
        train_end = self.trainingToDate.dateTime()

        try:
            trainPredict, trainY, testPredict, testY = self.service_invoker.start_training(train_start, train_end)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
            return


        print("\nCalculating error...")
        scorer = Scorer()
        trainScore, testScore = scorer.get_rmse_score(trainY, trainPredict, testY, testPredict)
        print('Train Score: %.2f RMSE' % (trainScore))
        print('Test Score: %.2f RMSE' % (testScore))
        trainScore, testScore = scorer.get_mape_score(trainY, trainPredict, testY, testPredict)
        print('Train Score: %.2f MAPE' % (trainScore))
        print('Test Score: %.2f MAPE' % (testScore))
        # self.plot(testPredict, 'w', "prediction")
        # self.plot(testY, 'r', "actual")
        print("\n\n--------------------------------------------------------\n")
        custom_plotting = Plotting()
        custom_plotting.show_plots(testPredict, testY)


    def load_model_for_prediction(self):
        return None

    def predict_power_consumption(self):
        prediction_begin = self.predictionFromDate.dateTime()
        if prediction_begin < self.min_date:
            QMessageBox.critical(self, "Error", 'Invalid dates', QMessageBox.Ok)
            return

        length_in_days = self.dateCountBox
        return None

    def __del__(self):
        sys.stdout = sys.__stdout__