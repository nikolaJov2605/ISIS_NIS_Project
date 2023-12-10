from datetime import datetime
import pandas

class SolarRadiationPreparation:
    def __init__(self) -> None:
        pass

    def preprocess_radiation_data(self):
        filename = "D:/Fakultet/Master/Inteligentni softverski infrastrukturni sistemi/Projekat/ISIS_NIS_Project/data/solar_radiation_data.xlsx"
        relevant_cols = ["time", "G(i)"]
        exc_radiation = pandas.read_excel(filename, usecols=relevant_cols)

        df = pandas.DataFrame()
        df['time'] = pandas.to_datetime(exc_radiation['time'], format='%Y%m%d:%H%M').dt.strftime('%Y-%m-%d %H:00:00')
        df['irradiance'] = exc_radiation['G(i)']

        df.to_csv('solar_radiation.csv', index=False)

        return df