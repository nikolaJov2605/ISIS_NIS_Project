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
from load_forecast.training.model_loader import ModelLoader


class ForecastServiceInvoker:
    def __init__(self) -> None:
        self.database_manager = DatabaseManager()
        self.ann_regression = AnnRegression()

        self.preprocessed_data = pandas.DataFrame()

    def preprocess_radiation_data(self):
        srp = SolarRadiationPreparation()
        radiation_df = srp.preprocess_radiation_data()
        return radiation_df

    def preprocess_data(self, path_to_data):
        data_converter = DataConverter(path_to_data)
        self.preprocessed_data = data_converter.load_and_convert_data()

    def get_min_date(self):
        return min(self.preprocessed_data['_time'])

    def get_min_date_from_dataset(self, dataset):
        return min(dataset['_time'])

    def get_max_date(self):
        return max(self.preprocessed_data['_time'])

    def get_max_date_from_dataset(self, dataset):
        return max(dataset['_time'])

    def write_data_to_database(self, path_to_data):
        self.preprocess_data(path_to_data)
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
        #starting_date = starting_date.toString('yyyy-MM-dd')
        #ending_date = ending_date.toString('yyyy-MM-dd')

        data_preparer = DataPreparer(starting_date, ending_date)
        trainX, trainY, testX, testY = data_preparer.prepare_for_training()
        time_begin = time.time()
        trainPredict, testPredict = self.ann_regression.compile_fit_predict(trainX, trainY, testX, do_training)
        time_end = time.time()
        print('Training duration: %.2f seconds' % (time_end - time_begin))

        trainPredict, trainY, testPredict, testY = data_preparer.inverse_transform(trainPredict, testPredict)

        return trainPredict, trainY, testPredict, testY


    def load_existing_trained_model_and_predict(self, starting_date, ending_date, do_training):
        #trainPredict, testPredict = self.ann_regression.get_selected_model(model_path, )

        dataframe = self.database_manager.read_measures_from_database_by_time(starting_date, ending_date)
        min_date = datetime.min

        try:
            min_date = self.get_min_date_from_dataset(dataframe)
        except:
            raise Exception("Invalid date input")
        if starting_date < min_date:
            raise Exception("Invalid date input")

        loader = ModelLoader(starting_date, ending_date)
        trainX, trainY, testX, testY = loader.prepare_model_for_prediction()

        trainPredict, testPredict = self.ann_regression.compile_fit_predict(trainX, trainY, testX, do_training)

        trainPredict, trainY, testPredict, testY = loader.inverse_transform(trainPredict, testPredict)

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

    def export_results(self, starting_date, ending_date):
        dataframe = self.database_manager.read_measures_from_database_by_time(starting_date, ending_date)
        time_load_dataframe = dataframe[["_time", "load"]]
        #exc_weather.to_csv('weather.csv', index=False)
        time_load_dataframe.to_csv('time_load.csv', index=False)

        write_data = self.database_manager.write_to_database(time_load_dataframe, 'Results')
        if write_data == False:
            raise Exception("Writing to database failed")

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
