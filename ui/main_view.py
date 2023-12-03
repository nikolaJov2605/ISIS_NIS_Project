from datetime import timedelta
import sys
import threading
import time
import pandas
import numpy
import pyqtgraph

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from database.database_manager import DatabaseManager
from load_forecast.data_converter import DataConverter
from load_forecast.training.data_preparer import DataPreparer
from load_forecast.training.ann_regression import AnnRegression
from load_forecast.scorer import Scorer
from load_forecast.plotting import Plotting
from optimization.generator_model_loader.model_loader import GeneratorModelLoader
from ui.service_invoker import ServiceInvoker
#from front.stream import Stream

class MainWindow(QMainWindow):
    file = None
    loaded_model_name = None
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("ui/frontend.ui", self)

        self.button_connections()

        self.file = None
        self.loaded_model_name = ''

        self.service_invoker = ServiceInvoker()

        generator_model = GeneratorModelLoader()


       # sys.stdout = Stream(newText=self.onUpdateText)

        #x = threading.Thread(target=self.listen)
        #x.start()

    # def write_to_database_thread(self):
    #     x = threading.Thread(target=self.write_to_database)
    #     x.start()

    # def start_ann_thread(self):
    #     x = threading.Thread(target=self.start_ann)
    #     x.start()

    def button_connections(self):
        self.browseCSVButton.clicked.connect(self.browse_files)
        self.browseModelButton.clicked.connect(self.browse_model)
        self.saveButton.clicked.connect(self.write_to_database)
        #self.trainButton.clicked.connect(self.start_ann_thread)
        self.trainButton.clicked.connect(self.start_ann)
        #self.loadModelButton.clicked.connect(self.load_model_for_prediction)
        self.predictButton.clicked.connect(self.predict_power_consumption)
        self.resultsButton.clicked.connect(self.filter_results)


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

        train_start = self.trainingFromDate.dateTime().toPyDateTime()
        train_end = self.trainingToDate.dateTime().toPyDateTime()

        try:
            trainPredict, trainY, testPredict, testY = self.service_invoker.start_training(train_start, train_end, do_training=True)
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


    # def load_model_for_prediction(self):
    #     train_start = self.predictionFromDate.dateTime()
    #     return None

    def predict_power_consumption(self):
        prediction_begin = self.predictionFromDate.dateTime().toPyDateTime()
        #prediction_begin = self.predictionFromDate.toPyDateTime()
        length_in_days = self.dayCountBox.value()
        prediction_end = prediction_begin + timedelta(days=length_in_days - 1)  #substracting one day because db_manager is adding one when quierying and another one because it is already included (condition in query is >=)
        try:
            result = self.service_invoker.load_existing_trained_model_and_predict(prediction_begin, prediction_end, do_training=False)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
            return

        try:
            result_dataframe = self.service_invoker.export_results(prediction_begin, prediction_end)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
            return

        self.populate_table(result_dataframe)

        # header = self.tableResults.horizontalHeader()

        # #header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        # for i in range(result_dataframe.shape[1]):
        #     header.setSectionResizeMode(i, QHeaderView.ResizeMode.Strech)#ResizeToContents)
        # #self.tableResults.resizeColumnsToContents()


    def filter_results(self):
        starting_date = self.resultsFromDate.dateTime().toPyDateTime()
        ending_date = self.resultsToDate.dateTime().toPyDateTime()
        filtered_data = self.service_invoker.filter_results(starting_date, ending_date)

        self.populate_table(filtered_data)


    def populate_table(self, dataframe):
        self.tableResults.setRowCount(dataframe.shape[0])
        self.tableResults.setColumnCount(dataframe.shape[1])

        self.tableResults.setHorizontalHeaderLabels(list(dataframe.columns))

        for i in range(dataframe.shape[0]):
            for j in range(dataframe.shape[1]):
                item = QTableWidgetItem(str(dataframe.iloc[i, j]))
                item.setTextAlignment(Qt.AlignHCenter)
                self.tableResults.setItem(i, j, item)

        self.tableResults.horizontalHeader().setStretchLastSection(True)
        self.tableResults.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def __del__(self):
        sys.stdout = sys.__stdout__