import numpy
import pandas
#from database.data_manager import DataManager
from sklearn.preprocessing import MinMaxScaler
from database.database_manager import DatabaseManager

#from database.database_manager import DatabaseManager
from load_forecast.training.data_helper import DataHelper

SHARE_FOR_TRAINING = 0.85

MIN_LOAD = 11575
MAX_LOAD = 30955

class DataPreparer:
    def __init__(self):
        self.data_helper = DataHelper()
        #self.scaler = MinMaxScaler(feature_range=(0, 1))
        #dataframe = self.data_helper.load_data_from_database(training_start, training_end)
        #self.number_of_columns = len(dataframe.columns)
        #self.datasetOrig = dataframe.values
        #self.datasetOrig = self.datasetOrig.astype('float32')
        #self.predictor_column_no = self.number_of_columns - 1
        #self.share_for_training = SHARE_FOR_TRAINING

    # def load_data_from_database(self, starting_time, ending_time):
    #     database_manager = DatabaseManager()
    #     dataframe = database_manager.read_from_database_by_time(starting_time, ending_time)
    #     #del dataframe['index']
    #     del dataframe['_time']
    #     dataframe.to_csv('db_measures.csv', index=False)
    #     return dataframe


    def prepare_for_training(self, date_start, date_end):
        self.prepare_dataframe(date_start, date_end)

        train_size = int(len(self.dataset_values) * SHARE_FOR_TRAINING)                    #velicina podataka za trening
        train, test = self.dataset_values[0:train_size,:], self.dataset_values[train_size:len(self.dataset_values),:]   # definicija setova za trening i test

        trainX, trainY = self.data_helper.create_dataset(train, self.number_of_columns)              # podela na zavisne i nezavisne podatke
        testX, testY = self.data_helper.create_dataset(test, self.number_of_columns)

        trainX = self.scale_data(trainX)
        testX = self.scale_data(testX)
        trainY = self.scale_load(trainY)
        testY = self.scale_load(testY)

        trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

        self.trainX = trainX
        self.trainY = trainY
        self.testX = testX
        self.testY = testY

        return trainX.copy(), trainY.copy(), testX.copy(), testY.copy()
    

    def prepare_data_for_prediction(self, start_date, end_date):
        self.dataframe = self.data_helper.load_data_from_database(start_date, end_date)

        self.number_of_columns = len(self.dataframe.columns)
        self.predictor_column_no = self.number_of_columns - 1

        predict_dataset_values = self.dataframe.values
        predict_dataset_values = predict_dataset_values.astype('float32')

        X_test, y_test = self.data_helper.create_dataset(predict_dataset_values, len(self.dataframe.columns))

        X_test = self.scale_data(X_test)
        y_test = self.scale_load(y_test)

        print(y_test)

        X_test = numpy.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

        self.testX = X_test
        self.testY = y_test

        return X_test.copy(), y_test.copy()



    def prepare_testing_data(self, starting_date, ending_date):
        self.dataframe = self.data_helper.load_data_from_database(starting_date, ending_date)
        self.dataframe_test = self.data_helper.load_testing_data_from_database(starting_date, ending_date)

        number_of_columns = len(self.dataframe_test.columns)

        predict_dataset_values = self.dataframe_test.values
        predict_dataset_values = predict_dataset_values.astype('float32')

        X_test = predict_dataset_values
        X_test = self.scale_data(X_test)

        X_test = numpy.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

        self.testX = X_test

        return X_test.copy()


    def prepare_dataframe(self, start_date, end_date):
        self.dataframe = self.data_helper.load_data_from_database(start_date, end_date)

        self.dataset_values = self.dataframe.values
        self.dataset_values = self.dataset_values.astype('float32')

        self.number_of_columns = len(self.dataframe.columns)
        self.predictor_column_no = self.number_of_columns - 1


    def get_min_load(self):
        return MAX_LOAD
        #return min(self.dataframe['load'])

    def get_max_load(self):
        return MIN_LOAD
        #return max(self.dataframe['load'])

    def scale_data(self, data):
        val = data / 100
        return val

    def scale_load(self, load):
        val = (load - self.get_min_load()) / (self.get_max_load() - self.get_min_load())
        return val.ravel()

    def scale_back(self, data):
        val = data * (self.get_max_load() - self.get_min_load()) + self.get_min_load()
        return val.ravel()

