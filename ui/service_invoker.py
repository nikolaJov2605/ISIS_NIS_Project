import time
import pandas
from database.database_manager import DatabaseManager
from load_forecast.data_converter import DataConverter
from load_forecast.training.ann_regression import AnnRegression
from load_forecast.training.data_preparer import DataPreparer


class ServiceInvoker:
    def __init__(self) -> None:
        self.database_manager = DatabaseManager()
        self.ann_regression = AnnRegression()

        self.preprocessed_data = pandas.DataFrame()


    def preprocess_data(self, path_to_data):
        data_converter = DataConverter(path_to_data)
        self.preprocessed_data = data_converter.load_and_convert_data()

    def get_min_date(self):
        return min(self.preprocessed_data['_time'])

    def get_max_date(self):
        return max(self.preprocessed_data['_time'])

    def write_data_to_database(self, path_to_data):
        self.preprocess_data(path_to_data)

        write_data = self.database_manager.write_to_database(self.preprocessed_data)
        if write_data == False:
            raise Exception("Date provided can't be in the past")

        return self.preprocessed_data, True

    def start_training(self, starting_date, ending_date):
        min_date = self.get_min_date()
        max_date = self.get_max_date()
        if ending_date <= starting_date or starting_date < min_date or starting_date > max_date:
            raise Exception("Invalid date input")
        starting_date = starting_date.toString('yyyy-MM-dd')
        ending_date = ending_date.toString('yyyy-MM-dd')

        data_preparer = DataPreparer(starting_date, ending_date)
        trainX, trainY, testX, testY = data_preparer.prepare_for_training()
        time_begin = time.time()
        trainPredict, testPredict = self.ann_regression.compile_fit_predict(trainX, trainY, testX)
        time_end = time.time()
        print('Training duration: %.2f seconds' % (time_end - time_begin))

        trainPredict, trainY, testPredict, testY = data_preparer.inverse_transform(trainPredict, testPredict)

        return trainPredict, trainY, testPredict, testY


    def load_existing_trained_model(self, model_path):
        trainPredict, testPredict = self.ann_regression.get_selected_model(model_path, )