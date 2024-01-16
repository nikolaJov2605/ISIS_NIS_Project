import numpy
import pandas
from load_forecast.scorer import Scorer
from load_forecast.training.ann_regression import AnnRegression

from load_forecast.training.data_helper import DataHelper
from load_forecast.training.data_preparer import DataPreparer


class Prediction():
    def __init__(self) -> None:
        self.data_helper = DataHelper()
        self.data_preparer = DataPreparer()
        self.ann_regression = AnnRegression()
        self.scorer = Scorer()

    def predict(self, start_date, end_date):
        X_test, y_test = self.data_preparer.prepare_data_for_prediction(start_date, end_date)

        y_predicted = self.ann_regression.predict(X_test)

        y_predicted = self.data_preparer.scale_back(y_predicted)
        y_test = self.data_preparer.scale_back(y_test)

        rmsr = self.scorer.get_mean_square_error(y_test.ravel(), y_predicted.ravel())
        print(f"RMSE: {rmsr}")

        mape = self.scorer.get_mean_absolute_percentage_error(y_test.ravel(), y_predicted.ravel())
        print(f'MAPE: {mape}%')

        return y_test, y_predicted



    def test_predict(self, date_start, date_end):
        X_test = self.data_preparer.prepare_testing_data(date_start, date_end)
        y_predicted = self.ann_regression.predict(X_test)

        y_predicted = self.data_preparer.scale_back(y_predicted)

        time_difference = date_end - date_start

        difference_in_hours = time_difference.total_seconds() / 3600 + 24
        dates = pandas.date_range(date_start, periods=difference_in_hours, freq='H')

        data_frame = pandas.DataFrame({'_time': dates, 'load': y_predicted.ravel()})


        return data_frame