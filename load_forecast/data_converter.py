import pandas
import numpy
from load_forecast.data_preparation.solar_radiation_preparation import SolarRadiationPreparation
from load_forecast.data_preparation.time_preparation import TimePreparer
from load_forecast.data_preparation.weather_preparation import WeatherPreparer
from load_forecast.data_preparation.load_preparation import LoadPreparer

class DataConverter:
    def __init__(self, filename):
        self.filename = filename


    def load_and_convert_data(self, testing: bool):
        # ----------------------------- WEATHER COLLECTION ----------------------------- #



        #TEMPERATURE, WINDSPEED, HUMIDITY, CLOUDCOVER
        # T, Ff, N, U
        #weather_cols = ["Local time", "T", "Po", "P", "Pa", "U", "DD", "Ff", "N", "WW", "W1", "W2"]
        weather_cols = ["Local time", "T", "U", "Ff", "N"]
        exc_weather = pandas.read_excel(self.filename, sheet_name='weather', usecols=weather_cols)

        exc_weather.rename(columns={'Local time':'_time'}, inplace=True)
        exc_weather['_time'] = pandas.to_datetime(exc_weather['_time'], dayfirst=True)

        wp = WeatherPreparer()
        exc_weather = wp.prepare_weather_data(exc_weather, testing)

        #exc_weather.to_csv('weather.csv', index=False)

        if testing:
            tp = TimePreparer(exc_weather)
            exc_weather = tp.add_time_fields()
            return exc_weather

        # ----------------------------- LOAD COLLECTION ----------------------------- #


        load_cols = ["DateShort", "TimeFrom", "TimeTo", "Load (MW/h)"]
        exc_load = pandas.read_excel(self.filename, sheet_name='load', usecols=load_cols)

        lp = LoadPreparer()
        exc_load = lp.reorder_load_data(exc_load)

        #exc_load.to_csv('load.csv', index=False)


        # --------------------------- MEARGED COLLECTIONS --------------------------- #

        measures = pandas.merge(exc_weather, exc_load, on='_time', how='left')

        # del measures['Local time']
        tp = TimePreparer(measures)


        measures = tp.add_time_fields()


        #measures.to_csv('measures.csv', index=False)

        return measures

        # -------------------------------------------------------------------------- #