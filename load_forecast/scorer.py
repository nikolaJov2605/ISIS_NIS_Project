import math
import numpy
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
class Scorer:

    def get_rmse_score(self, train_y, train_predict, test_y, test_predict):
        train_score = math.sqrt(mean_squared_error(train_y, train_predict))
        test_score = math.sqrt(mean_squared_error(test_y, test_predict))
        return train_score, test_score


    def get_mape_score(self, train_y, train_predict, test_y, test_predict):
        train_score = self.get_mean_absolute_percentage_error(train_y, train_predict)
        test_score = self.get_mean_absolute_percentage_error(test_y, test_predict)

        return train_score, test_score


    def get_mean_absolute_percentage_error(self, y_actual, y_predicted):
        mape = numpy.mean(numpy.abs((y_actual - y_predicted)/y_actual))*100
        return mape

    def get_mean_square_error(self, y_actual, y_predicted):
        rmes = math.sqrt(mean_squared_error(y_actual, y_predicted))
        return rmes