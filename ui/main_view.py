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
#from front.stream import Stream

class MainWindow(QMainWindow):
    file = None
    loaded_model_name = None
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("ui/frontend.ui", self)
        self.browseCSVButton.clicked.connect(self.browse_files)
        self.browseModelButton.clicked.connect(self.browse_model)
        self.saveButton.clicked.connect(self.load_to_database_thread)
        #self.trainButton.clicked.connect(self.start_ann_thread)
        self.trainButton.clicked.connect(self.start_ann)


       # sys.stdout = Stream(newText=self.onUpdateText)

        #x = threading.Thread(target=self.listen)
        #x.start()

    def load_to_database_thread(self):
        x = threading.Thread(target=self.load_to_database)
        x.start()

    def start_ann_thread(self):
        x = threading.Thread(target=self.start_ann)
        x.start()

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
            self.trainButton.setEnabled(True)
            self.file = None
            self.importCSVEdit.setText('')

    def load_to_database(self):
        if self.file is None:
            return

        print("Loading and converting data...")
        importCSVEdit = "data/" + self.importCSVEdit.text()#.split('/')[-1]
        data_converter = DataConverter(importCSVEdit)
        preprocessed_data = data_converter.load_and_convert_data()

        self.max_date = max(preprocessed_data['_time'])
        self.min_date = min(preprocessed_data['_time'])


        print("\nDone.")
        print("\nWriting to database...")
        time1 = time.time()
        database_manager = DatabaseManager()
        write_data = database_manager.write_to_database(preprocessed_data)
        if write_data == False:
            print("An error occurred while writing to database")
            return False
       # data_writer = DataWriter(ret_data)
       # data_writer.write_to_database()
        time2 = time.time()
        print("\nDone.")
        print('Writing to database duration: %.2f seconds' % (time2 - time1))

        self.converted_data = preprocessed_data
        if self.converted_data is not None:
            self.trainButton.setEnabled(True)
        return True

    def start_ann(self):
        model_loaded = False
        if self.loaded_model_name is not None:
            model_loaded = True
        else:
            self.loaded_model_name = ''

        train_start = self.trainingFromDate.dateTime()
        train_end = self.trainingToDate.dateTime()

        if train_end <= train_start or train_start < self.min_date or train_end > self.max_date:
            QMessageBox.critical(self, "Error", 'Invalid dates', QMessageBox.Ok)
            return
        train_start = train_start.toString('yyyy-MM-dd')
        train_end = train_end.toString('yyyy-MM-dd')
        print("\nPreparing data...")
        data_preparer = DataPreparer(train_start, train_end)
        trainX, trainY, testX, testY = data_preparer.prepare_for_training()
        print("\nDone.")
        print("Doing some learning...")
        ann_regression = AnnRegression()
        time_begin = time.time()
        trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX, self.loaded_model_name)
        time_end = time.time()
        print('Training duration: %.2f seconds' % (time_end - time_begin))

        trainPredict, trainY, testPredict, testY = data_preparer.inverse_transform(trainPredict, testPredict)


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


    def __del__(self):
        sys.stdout = sys.__stdout__