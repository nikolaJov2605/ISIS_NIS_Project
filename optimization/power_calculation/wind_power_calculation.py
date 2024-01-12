from datetime import timedelta
from database.database_manager import DatabaseManager
from optimization.generator_model.wind_generator import WindGenerator
from optimization.generator_model_loader.model_loader import GeneratorModelLoader
import math

AIR_DENCITY = 1.204

class WindPowerCalculation:
    def __init__(self, generator_count, optimization_date) -> None:
        self.wind_generator: WindGenerator = GeneratorModelLoader.get_wind_generator()
        self.database_manager = DatabaseManager()
        self.generator_count = generator_count
        self.weather_data = self.load_wind_data(optimization_date)

    def calculate_hourly_power(self):
        hourly_power = []

        for wind_speed in self.weather_data['Ff']: #wind speed
            if self.is_in_boundries(wind_speed):
                power = 0.5 * (self.wind_generator.efficiency/100) * AIR_DENCITY * pow(self.wind_generator.blade_length, 2) * math.pi * pow(wind_speed, 3) *  self.generator_count
                power_in_mw = power / 1_000_000
                hourly_power.append(power_in_mw)
            else:
                hourly_power.append(0)

        return hourly_power

    def is_in_boundries(self, windspeed: int):
        if windspeed >= self.wind_generator.cut_in_speed and windspeed <= self.wind_generator.cut_out_speed:
            return True
        else:
            return False


    def load_wind_data(self, optimization_date):
        #optimization_date =optimization_date.dateTime().toPyDateTime()
        length_in_days = 1
        ending_date = optimization_date + timedelta(days=length_in_days - 1)
        dataframe = self.database_manager.read_measures_from_database_by_time(optimization_date, ending_date)
        ret_df = dataframe[['_time', 'Ff']]
        return ret_df