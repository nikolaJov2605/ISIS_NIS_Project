from time import time
from load_forecast.scorer import Scorer
from load_forecast.training.ann_regression import AnnRegression
from load_forecast.training.data_preparer import DataPreparer


class ModelCreator():
    def __init__(self) -> None:
        self.preparer = DataPreparer()

    def generate_model(self, starting_date, ending_date):
        trainX, trainY, testX, testY = self.preparer.prepare_for_training(starting_date, ending_date)

        ann_regression = AnnRegression()

        time_begin = time()
        trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX, True, trainX.shape[2])
        time_end = time()

        print('Training duration: ' + str((time_end - time_begin)) + ' seconds')


        trainY = self.preparer.scale_back(trainY)
        testY = self.preparer.scale_back(testY)
        trainPredict = self.preparer.scale_back(trainPredict)
        testPredict = self.preparer.scale_back(testPredict)


        scorer = Scorer()
        trainScore, testScore = scorer.get_rmse_score(trainY, trainPredict, testY, testPredict)
        print('Train Score: %.2f RMSE' % (trainScore))
        print('Test Score: %.2f RMSE' % (testScore))

        trainScore, testScore = scorer.get_mape_score(trainY, trainPredict, testY, testPredict)
        print(f'Train Score: {round(trainScore, 2)}% MARE')
        print(f'Test Score: {round(testScore, 2)}% MARE')

        return testPredict, testY


