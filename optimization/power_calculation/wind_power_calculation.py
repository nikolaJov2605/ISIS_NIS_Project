from optimization.generator_model.wind_generator import WindGenerator
from optimization.generator_model_loader.model_loader import GeneratorModelLoader
import math

AIR_DENCITY = 1.204

class WindPowerCalculation:
    def __init__(self, generator_count, weather_data) -> None:
        self.wind_generator: WindGenerator = GeneratorModelLoader.get_wind_generator()
        self.generator_count = generator_count
        self.weather_data = weather_data

    def calculate_hourly_power(self):
        hourly_power = []

        for wind_speed in self.weather_data['Ff']: #wind speed
            if self.is_in_boundries(wind_speed):
                power = 0.5 * (self.wind_generator.efficiency/100) * AIR_DENCITY * pow(self.wind_generator.blade_length, 2) * math.pi * pow(wind_speed, 3)
                power_in_mw = power / 1_000_000
                hourly_power.append(power_in_mw)
            else:
                hourly_power.append(0)

    def is_in_boundries(self, windspeed: int):
        if windspeed >= self.wind_generator.cut_in_speed and windspeed <= self.wind_generator.cut_out_speed:
            return True
        else:
            return False