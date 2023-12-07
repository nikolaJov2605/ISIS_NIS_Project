from optimization.generator_model_loader.model_loader import GeneratorModelLoader

import pandas
import pvlib

# Serbia latitude and longitude
LATITUDE = 44.2107675
LONGITUDE = 20.9224158

class SolarPowerCalculator:
    def __init__(self, generator_count: int) -> None:
        self.solar_generator = GeneratorModelLoader.solar_genereator
        self.generator_count = generator_count

    def calculate_solar_generator_hourly_power(self, start_date, end_date):
        solar_irradiance = self.calculate_solar_irradiance(start_date, end_date)

    def calculate_solar_irradiance(self, start_date, end_date):
        st_date = start_date.toString('yyyy-MM-dd')
        e_date = end_date.toString('yyyy-MM-dd')
        # Create a sample time series
        times = pandas.date_range(st_date, e_date, freq='H', tz='Etc/GMT+1')
        latitude, longitude = LATITUDE, LONGITUDE
        data = pandas.DataFrame({'ghi': [100] * len(times)}, index=times)

        # Specify the PV system location
        #location = pvlib.location.Location(latitude, longitude)

        # Calculate solar position
        solar_position = pvlib.solarposition.get_solarposition(times, latitude, longitude)

        # Calculate extraterrestrial radiation
        dni_extra = pvlib.irradiance.get_extra_radiation(times)

        # Calculate solar radiation on a tilted surface (using Hay-Davies model)
        tilt = 30  # degrees
        azimuth = 180  # degrees (south-facing)
        surface_irradiance = pvlib.irradiance.get_total_irradiance(
            surface_tilt=tilt,
            surface_azimuth=azimuth,
            solar_zenith=solar_position['apparent_zenith'],
            solar_azimuth=solar_position['azimuth'],
            dni=dni_extra,
            ghi=data['ghi'],
            dhi=data['ghi'] * 0.2  # Example diffuse fraction
        )

        return surface_irradiance


