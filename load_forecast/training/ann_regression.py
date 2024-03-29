from datetime import datetime
import os
from keras.layers import Dense
from keras.models import Sequential
from tensorflow import keras
from load_forecast.training.ann_base import AnnBase

MODEL_PATH = "load_forecast/trained_models"
MODEL_NAME = 'model'
TRAINED_MODEL = '/model_33_2024-01-16_11_17_33'
class AnnRegression(AnnBase):
    def model_naming(self):
        model_cnt = 0
        for _, dirnames, filenames in os.walk(MODEL_PATH):
            model_cnt += len(dirnames)
        date = datetime.now()
        date_date = date.date()
        date_time_hours = date.time().hour
        date_time_minutes = date.time().minute
        date_time_seconds = date.time().second

        name =  MODEL_PATH + "/" + MODEL_NAME + "_" + str(model_cnt) + "_" + str(date_date) + "_" + str(date_time_hours) + "_" +  str(date_time_minutes) + "_" +  str(date_time_seconds)

        return name

    def get_model(self, size_shape):
        model = Sequential()
        if self.number_of_hidden_layers > 0:
           model.add(Dense(self._number_of_neurons_in_first_hidden_layer, input_shape=(1, size_shape), kernel_initializer=self.kernel_initializer, activation=self.activation_function))
           if self.number_of_hidden_layers > 1:
               for i in range(self.number_of_hidden_layers - 1):
                   model.add(Dense(self.number_of_neurons_in_other_hidden_layers, kernel_initializer=self.kernel_initializer, activation=self.activation_function))
        model.add(Dense(1, kernel_initializer=self.kernel_initializer))
        return model

    def get_model_from_path(self, path):
        model = keras.models.load_model(path)
        return model


    def compile_and_fit(self, trainX, trainY, size_shape):
        self.model = self.get_model(size_shape)
        self.trainX = trainX
        self.model.compile(loss=self.cost_function, optimizer=self.optimizer)
        self.model.fit(trainX, trainY, epochs=self.epoch_number, batch_size=self.batch_size_number, verbose=self.verbose)
        model_name = self.model_naming()
        self.model.save(model_name)    # model se sacuva u neki json

    def use_current_model(self, path, trainX):
        self.trainX = trainX
        self.model = self.get_model_from_path(path)

    def get_predict(self, testX):
        trainPredict = self.model.predict(self.trainX)
        testPredict = self.model.predict(testX)
        return trainPredict, testPredict

    def get_selected_model(self, loaded_model_name, trainX, testX):
        self.use_current_model(loaded_model_name, trainX)     #ucitavanje modela
        return self.get_predict(testX)

    def compile_fit_predict(self, trainX, trainY, testX, do_training, size_shape):
        if do_training:
            self.compile_and_fit(trainX, trainY, size_shape)
        else:
            self.use_current_model(MODEL_PATH + TRAINED_MODEL, trainX)
        return self.get_predict(testX)
    

    def predict(self, X_test):
        #self.use_current_model(MODEL_PATH + TRAINED_MODEL, X_test)
        self.model = self.get_model_from_path(f'{MODEL_PATH}\\{TRAINED_MODEL}')
        y_predict = self.model.predict(X_test)
        return y_predict

