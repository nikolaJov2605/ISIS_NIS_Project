from datetime import datetime
import time
import pandas
from database.database_manager import DatabaseManager
from load_forecast.data_converter import DataConverter
from load_forecast.data_preparation.solar_radiation_preparation import SolarRadiationPreparation
from load_forecast.plotting import Plotting
from load_forecast.scorer import Scorer
from load_forecast.training.ann_regression import AnnRegression
from load_forecast.training.data_preparer import DataPreparer
from load_forecast.training.model_creator import ModelCreator
from load_forecast.training.prediction import Prediction


class ForecastServiceInvoker:
    def __init__(self) -> None:
        self.database_manager = DatabaseManager()
        self.ann_regression = AnnRegression()

        self.preprocessed_data = pandas.DataFrame()

    def preprocess_radiation_data(self):
        srp = SolarRadiationPreparation()
        radiation_df = srp.preprocess_radiation_data()
        return radiation_df

    def preprocess_data(self, path_to_data, testing: bool):
        data_converter = DataConverter(path_to_data)
        self.preprocessed_data = data_converter.load_and_convert_data(testing)

    def get_min_date(self):
        return min(self.preprocessed_data['_time'])

    def get_min_date_from_dataset(self, dataset):
        return min(dataset['_time'])

    def get_max_date(self):
        return max(self.preprocessed_data['_time'])

    def get_max_date_from_dataset(self, dataset):
        return max(dataset['_time'])

    def write_test_data_to_database(self, path_to_data):
        self.preprocess_data(path_to_data, testing=True)

        write_data = self.database_manager.write_to_database(self.preprocessed_data, 'TestMeasures')
        if write_data == False:
            raise Exception("Writing testing measurment data to database failed!")

        return self.preprocessed_data, True

    def write_data_to_database(self, path_to_data):
        self.preprocess_data(path_to_data, testing=False)
        solar_radiation_data = self.preprocess_radiation_data()

        write_data = self.database_manager.write_to_database(self.preprocessed_data, 'Measures')
        if write_data == False:
            raise Exception("Writing measurment data to database failed")

        write_radiation_data = self.database_manager.write_to_database(solar_radiation_data, 'SolarRadiation')
        if write_data == False:
            raise Exception("Writing solar radiation data to database failed")

        return self.preprocessed_data, True

    def start_training(self, starting_date, ending_date, do_training):
        min_date = self.get_min_date()
        max_date = self.get_max_date()
        if ending_date <= starting_date or starting_date < min_date or starting_date > max_date:
            raise Exception("Invalid date input")

        modelCreator = ModelCreator()
        y_predicted, y_test = modelCreator.generate_model(starting_date, ending_date)

        return y_predicted, y_test


    def load_existing_trained_model_and_predict(self, starting_date, ending_date, do_training, testing: bool):
        dataframe = pandas.DataFrame()
        if not(testing):
            dataframe = self.database_manager.read_measures_from_database_by_time(starting_date, ending_date)
        else:
            dataframe = self.database_manager.read_testing_measures_from_database_by_time(starting_date, ending_date)

        min_date = datetime.min

        try:
            min_date = self.get_min_date_from_dataset(dataframe)
        except:
            raise Exception("Invalid date input")
        if starting_date < min_date:
            raise Exception("Invalid date input")


        if testing:
            prediction = Prediction()
            predicted_df = prediction.test_predict(starting_date, ending_date)
            self.database_manager.write_to_database(predicted_df, "Results")
        else:
            prediction = Prediction()
            y_test, y_predicted = prediction.predict(starting_date, ending_date)
            self.database_manager.write_to_database(y_predicted, "Results")

            plotting = Plotting()
            plotting.show_plots(y_predicted, y_test)


    def export_results(self, starting_date, ending_date):
        read_data = self.database_manager.read_from_database('Results')

        return read_data

    def write_optimization_data(self, data):
        write_data = self.database_manager.write_to_database(data, 'OptimizationDay')
        if write_data == False:
            raise Exception("Writing to database failed")

        return self.preprocessed_data, True

    def filter_results(self, starting_date, ending_date):
        dataframe = self.database_manager.read_results_from_database_by_time(starting_date, ending_date)
        return dataframe

    def read_db_table(self, table_name):
        table_data = self.database_manager.read_from_database(table_name)
        return table_data


