import datetime
import numpy
import pandas

# additional: Dewpoint Temperature, Amount of Precipitation, Horizontal Visibility
# relative humidity, mean wind speed, total cloud cover
WEATHER_COLS = ["Local time","T", "U", "Ff", "N"]

class WeatherPreparer():

    def fix_cloud_cover(self, data_frame):
        data_frame['N'] = numpy.where(data_frame['N'].str.contains('–'), data_frame['N'].str.replace('–', ' ', regex=False) , data_frame['N'])
        data_frame["N"] = data_frame['N'].str.split(pat=' ', n=-1, expand=True)[0]
        data_frame['N'] = numpy.where(data_frame['N']=='no', '0', data_frame['N'])
        data_frame['N'] = numpy.where(data_frame['N'].str.contains('%'), data_frame['N'].str.replace('%', '', regex=False) , data_frame['N'])
        data_frame['N'] = numpy.where(data_frame['N'].str.contains('.'), data_frame['N'].str.replace('.', '', regex=False) , data_frame['N'])
        data_frame['N'] = numpy.where(data_frame['N'].str.contains('Sky'), data_frame['N'].str.replace('Sky', '100', regex=False) , data_frame['N'])
        data_frame['N'] = data_frame['N'].astype('float') / 100
        return data_frame['N']

    def add_missing_entries(self, data_frame):
        for idx, row in data_frame.iterrows():
            one_hour = datetime.timedelta(hours=1)
            current_time = data_frame.iloc[idx]['time']
            next_time = data_frame.iloc[idx + 1]['time']
            #diff = datetime.timedelta(current_time, next_time)
            diff = next_time - current_time
            if diff > one_hour:
                # see how many rows are missing and add them
                for i in range(int(float(diff.total_seconds()) / 3600) - 1):
                    if current_time.hour == 23:
                        dt = datetime.datetime(next_time.year, next_time.month, next_time.day, next_time.hour + 1, next_time.minute, next_time.second)
                    else:
                        dt = datetime.datetime(current_time.year, current_time.month, current_time.day, current_time.hour + 1, current_time.minute, current_time.second)

                    df_temp = {'time': dt}
                    data_frame = data_frame._append(df_temp, ignore_index = True)


        data_frame = data_frame.sort_values(by=['time'])
        return data_frame


    def prepare_weather_data(self, data_frame):
        data_frame = self.add_missing_entries(data_frame)
        data_frame['U'] = self.fix_cloud_cover(data_frame)
        data_frame['U'] = data_frame['U'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both").round(decimals=1)
        data_frame['Ff'] = data_frame['Ff'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both").round(decimals=1)
        data_frame['N'] = data_frame['N'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both").round(decimals=1)

        data_frame['T'] = data_frame['T'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both").round(decimals=1)

        return data_frame
