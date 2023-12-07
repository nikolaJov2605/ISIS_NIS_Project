# import pandas as pd
# import pvlib

# # Create a sample time series
# times = pd.date_range('2022-01-01', '2022-01-02', freq='H', tz='UTC')
# latitude, longitude = 37.7749, -122.4194  # San Francisco coordinates
# data = pd.DataFrame({'ghi': [100] * len(times)}, index=times)

# # Specify the PV system location
# location = pvlib.location.Location(latitude, longitude)

# # Calculate solar position
# solar_position = pvlib.solarposition.get_solarposition(times, latitude, longitude)

# # Calculate extraterrestrial radiation
# dni_extra = pvlib.irradiance.get_extra_radiation(times)

# # Calculate solar radiation on a tilted surface (using Hay-Davies model)
# tilt = 30  # degrees
# azimuth = 180  # degrees (south-facing)
# surface_irradiance = pvlib.irradiance.get_total_irradiance(
#     surface_tilt=tilt,
#     surface_azimuth=azimuth,
#     solar_zenith=solar_position['apparent_zenith'],
#     solar_azimuth=solar_position['azimuth'],
#     dni=dni_extra,
#     ghi=data['ghi'],
#     dhi=data['ghi'] * 0.2  # Example diffuse fraction
# )

# print(surface_irradiance)





from datetime import datetime
import pandas

filename = "D:/Fakultet/Master/Inteligentni softverski infrastrukturni sistemi/Projekat/ISIS_NIS_Project/data/radiation.xlsx"
relevant_cols = ["time", "G(i)"]
exc_radiation = pandas.read_excel(filename, usecols=relevant_cols)

df = pandas.DataFrame()
df['time'] = pandas.to_datetime(exc_radiation['time'], format='%Y%m%d:%H%M').dt.strftime('%Y-%m-%d %H:00:00')

print(df)