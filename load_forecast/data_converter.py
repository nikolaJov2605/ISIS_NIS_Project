import pandas
import numpy
from load_forecast.data_preparation.solar_radiation_preparation import SolarRadiationPreparation
from load_forecast.data_preparation.time_preparation import TimePreparer
from load_forecast.data_preparation.weather_preparation import WeatherPreparer
from load_forecast.data_preparation.load_preparation import LoadPreparer
#from database.database import Database
#from database.data_manager import DataManager

class DataConverter:
    def __init__(self, filename):
        self.filename = filename


    def load_and_convert_data(self):
        # ----------------------------- WEATHER COLLECTION ----------------------------- #

        # Local time    - date and time
    ##### FEELS LIKE TEMPERATURE TO CALCULATE AND ADD
    ##### T             - air temperature - temperatura vazduha (U STEPENIMA CELZIJUSA)
    ##### Po            - Atmpspheric Pressure (milimeters of mercury) - VAZDUSNI PRITISAK (U MILIMETRIMA ZIVE)
        # Pa            - Pressure tendency: changes in atmospheric pressure over last three hours (milimeters of mercury)
        # P             - ?
        # U             - relative humidity (%)
    ##### DD            - mean wind direction (compass point) - PRAVAC VETRA (MOZDA IZRACUNATI U STEPENIMA)
        # Ff            - mean wind speed (meters per second)
    ##### ff10          - maximum gust value over 10-minutes period (meters per second) - NALETI VETRA U METRIMA PO SEKUNDI
    ##### ff3           - maximum gust value between periods of observation
        # N             - total cloud cover
    ##### WW            - presend weather reported from the weather station - TEKSTUALNI OPIS VREMENA
        # W1            - past weather 1
        # W2            - past weather 2
        # Tn            - minimum air temperature during the period (not exceeding 12 hours)
        # Tx            - maximum air temperature during the past period (not exceeding 12 hours)
        # Cl            - clouds of the hemera stratocumulus, stratus, cu,ulus and cumulonimbus
        # Nh            - amount of the CL cloud present or, if no CL cloud is present, the amount of the CM cloud present
        # H             - height of the base of base of the lowest cloud (m)
        # Cm            - clouds of the genera altocu,ulus, altrostratus and nimbostratus
        # Ch            - clouds of the genera cirrus, cirrocumulus and cirrostratus
        # VV            - horizontal visibility (km)
    ##### Td            - dewpoint temperature (degrees celsius) - TEMPERATURA ROSE
    ##### RRR           - amount of precipitation (milimeters) - PADAVINE U MILIMETRIMA
        # tR            - the period of time during which the specified amount of precipitation was accumulated
        # E             - state of the ground without snow or measurable ice cover
        # Tg            - the minimum soil surface temperature at night (degrees celsius)
        # E'            - state of the ground with snow or measurable ice cover
        # sss           - snow dept (cm)


        #TEMPERATURE, WINDSPEED, HUMIDITY, CLOUDCOVER
        # T, Ff, N, U
        #weather_cols = ["Local time", "T", "Po", "P", "Pa", "U", "DD", "Ff", "N", "WW", "W1", "W2"]
        weather_cols = ["Local time", "T", "U", "Ff", "N"]
        exc_weather = pandas.read_excel(self.filename, sheet_name='weather', usecols=weather_cols)

        exc_weather.rename(columns={'Local time':'_time'}, inplace=True)
        exc_weather['_time'] = pandas.to_datetime(exc_weather['_time'], dayfirst=True)

        wp = WeatherPreparer()
        exc_weather = wp.prepare_weather_data(exc_weather)

        #exc_weather.to_csv('weather.csv', index=False)


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