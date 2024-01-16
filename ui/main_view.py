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
from load_forecast.forecast_service_invoker import ForecastServiceInvoker
from ui.optimizer.optimization_tab import OptimizationTab
from ui.optimizer.optimization_configs.thermal_coal_configuration import ThermalCoalConfiguration
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

        self.service_invoker = ForecastServiceInvoker()

        generator_model = GeneratorModelLoader()
        generator_model.load_generator_models()

        # self.coal_generator_tab = CoalGeneratorTab(self.coal)
        self.optimization_tab = OptimizationTab(self.OptimizationTab)


    def button_connections(self):
        self.browseCSVButton.clicked.connect(self.browse_files)
        self.browseTestButton.clicked.connect(self.browse_test)
        self.saveButton.clicked.connect(self.write_to_database)
        self.trainButton.clicked.connect(self.start_ann)
        self.loadTestButton.clicked.connect(self.load_test_to_database)
        self.predictButton.clicked.connect(self.predict_power_consumption)
        self.resultsButton.clicked.connect(self.filter_results)
        self.exportButton.clicked.connect(self.export_day_data_for_optimization)


    def onUpdateText(self, text):
        cursor = self.textedit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textedit.setTextCursor(cursor)
        self.textedit.ensureCursorVisible()


    def browse_files(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open file', 'data', 'XLSX (*.xlsx)')
        self.importCSVEdit.setText(self.file[0].split('/')[-1])
        if self.file is not None:
            self.saveButton.setEnabled(True)
            self.loaded_model_name = None
            self.importTestEdit.setText('')

    def browse_test(self):
        self.test_file = QFileDialog.getOpenFileName(self, 'Open file', 'data', 'XLSX (*.xlsx)')
        self.importTestEdit.setText(self.test_file[0].split('/')[-1])
        if self.test_file is not None:
            self.loadTestButton.setEnabled(True)
            self.file = None
            self.importCSVEdit.setText('')

    def load_test_to_database(self):
        if self.test_file is None:
            return

        print("Loading and converting test data...")#
        importTestEdit = "drop_test_data_here/" + self.importTestEdit.text()

        try:
            self.preprocessed_data, function_result = self.service_invoker.write_test_data_to_database(importTestEdit)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
            return
        
        QMessageBox.information(self, "Info", 'Test data loaded to database!', QMessageBox.Ok)

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

        train_start = self.trainingFromDate.dateTime().toPyDateTime()
        train_end = self.trainingToDate.dateTime().toPyDateTime()

        try:
            testPredict, testY = self.service_invoker.start_training(train_start, train_end, do_training=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
            return

        plotting = Plotting()
        plotting.show_plots(testPredict, testY)

        QMessageBox.information(self, "Info", 'Training finished!', QMessageBox.Ok)


    def predict_power_consumption(self):
        testing = False
        if self.importTestEdit.text() != '':
            testing = True
        prediction_begin = self.predictionFromDate.dateTime().toPyDateTime()
        #prediction_begin = self.predictionFromDate.toPyDateTime()
        length_in_days = self.dayCountBox.value()
        prediction_end = prediction_begin + timedelta(days=length_in_days - 1)  #substracting one day because db_manager is adding one when quierying and another one because it is already included (condition in query is >=)
        try:
            result = self.service_invoker.load_existing_trained_model_and_predict(prediction_begin, prediction_end, do_training=False, testing=testing)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
            return

        try:
            result_dataframe = self.service_invoker.export_results(prediction_begin, prediction_end)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
            return

        self.populate_table(result_dataframe)

        self.exportButton.setEnabled(True)


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

    def export_day_data_for_optimization(self):
        results = self.service_invoker.read_db_table('Results')

        results['_time'] = pandas.to_datetime(results['_time'])
        results['date_part'] = results['_time'].dt.date
        min_date = results['date_part'].min()

        min_date_df = results[results['date_part'] == min_date]

        del min_date_df['date_part']

        try:
            self.service_invoker.write_optimization_data(min_date_df)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
            return

        self.optimization_tab.optimization_date = min_date
        self.optimization_tab.populate_table('daily_load_report_table', min_date_df)
        self.optimization_tab.calculate_daily_load()

    def __del__(self):
        sys.stdout = sys.__stdout__