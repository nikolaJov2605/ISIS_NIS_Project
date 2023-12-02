import numpy
from sklearn.preprocessing import MinMaxScaler

#from database.database_manager import DatabaseManager
from load_forecast.training.data_helper import DataHelper

SHARE_FOR_TRAINING = 0.85

class ModelLoader:
    def __init__(self, date_start, date_end):
        self.data_helper = DataHelper()
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        dataframe = self.data_helper.load_data_from_database(date_start, date_end)
        self.number_of_columns = len(dataframe.columns)
        self.datasetOrig = dataframe.values
        self.datasetOrig = self.datasetOrig.astype('float32')
        self.predictor_column_no = self.number_of_columns - 1
        self.share_for_training = SHARE_FOR_TRAINING


    def prepare_model_for_prediction(self):
        dataset = self.scaler.fit_transform(self.datasetOrig)
        #train_size = int(len(dataset) * self.share_for_training)
        #train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
        train, test = dataset[0:len(dataset),:], dataset[0:len(dataset),:]
        look_back = self.number_of_columns
        trainX, trainY = self.data_helper.create_dataset(train, look_back)
        testX, testY = self.data_helper.create_dataset(test, look_back)

        trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

        self.trainX = trainX
        self.trainY = trainY
        self.testX = testX
        self.testY = testY

        return trainX, trainY, testX, testY

    def inverse_transform(self, trainPredict, testPredict): # vracanje na prave vrednosti
        trainPredict = numpy.reshape(trainPredict, (trainPredict.shape[0], trainPredict.shape[1]))  # pakujemo dobijene load-ove u mnogo vrsta i jednu kolonu
        testPredict = numpy.reshape(testPredict, (testPredict.shape[0], testPredict.shape[1]))      # pakujemo test load-ove u mnogo vrsta i jednu kolonu
        self.trainX = numpy.reshape(self.trainX, (self.trainX.shape[0], self.trainX.shape[2]))      # trening nezavisni podaci prakticno, 10 kolona
        self.testX = numpy.reshape(self.testX, (self.testX.shape[0], self.testX.shape[2]))          # test nezavisni podaci, isto kao i trening, samo ih ima manje
        trainXAndPredict = numpy.concatenate((self.trainX, trainPredict),axis=1)    # trening podaci spojeni sa rezultatima predikcije
        testXAndPredict = numpy.concatenate((self.testX, testPredict),axis=1)       # test podaci spojeni sa test rezultatima predikcije
        trainY = numpy.reshape(self.trainY, (self.trainY.shape[0], 1))          # zavisni podaci trening skupa spakovani u kolonu
        testY = numpy.reshape(self.testY, (self.testY.shape[0], 1))             # zavisni podaci test skupa spakovani u kolonu
        trainXAndY = numpy.concatenate((self.trainX, trainY),axis=1)        # spojeni trening zavisni i nezavisni podaci
        testXAndY = numpy.concatenate((self.testX, testY),axis=1)           # spojeni test zavisni i nezavisni podaci
        trainXAndPredict = self.scaler.inverse_transform(trainXAndPredict)  # inverzno trening podaci spojeni sa rezultatima predikcije |=> ova dva
        trainXAndY = self.scaler.inverse_transform(trainXAndY)              # inverzno trening podaci zavisni i nezavisni               |
        testXAndPredict = self.scaler.inverse_transform(testXAndPredict)    # inverzno test podaci spojeni sa rezultatima predikcije |=> ova dva
        testXAndY = self.scaler.inverse_transform(testXAndY)                # inverzno test podaci zavisni i nezavisni               |
        trainPredict = trainXAndPredict[:,self.predictor_column_no]
        trainY = trainXAndY[:,self.predictor_column_no]
        testPredict = testXAndPredict[:,self.predictor_column_no]
        testY = testXAndY[:,self.predictor_column_no]
        return trainPredict, trainY, testPredict, testY

    # def load_data_from_database(self, starting_time, ending_time):
    #     database_manager = DatabaseManager()
    #     dataframe = database_manager.read_from_database_by_time(starting_time, ending_time)
    #     del dataframe['_time']
    #     #dataframe.to_csv('db_measures.csv', index=False)
    #     return dataframe

    # def create_dataset(self, dataset, look_back):
    #     dataX, dataY = [], []
    #     for i in range(len(dataset)-1):
    #         a = dataset[i, 0:look_back-1]
    #         dataX.append(a)
    #         dataY.append(dataset[i, look_back-1])
    #     return numpy.array(dataX), numpy.array(dataY)