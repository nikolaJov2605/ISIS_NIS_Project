import numpy

SECONDS_IN_DAY = 24 * 60 * 60
DAYS_IN_WEEK = 7
MONTHS_IN_YEAR = 12
SEASONS_IN_YEAR = 4

class TimePreparer:
    def __init__(self, data_frame) -> None:
        self.dataframe = data_frame

    def add_time_fields(self):
        self.insert_hours_columns()
        self.insert_day_columns()
        self.insert_month_collumns()

        #del self.dataframe['_time']
        return self.dataframe

    def insert_hours_columns(self):
        hours = self.dataframe['_time'].dt.hour
        seconds = hours * 3600
        sinus_time = numpy.sin(2 * numpy.pi * seconds / SECONDS_IN_DAY)
        cosinus_time = numpy.cos(2 * numpy.pi * seconds / SECONDS_IN_DAY)
        self.dataframe.insert(1, 'sin_time', sinus_time)
        self.dataframe.insert(1, 'cos_time', cosinus_time)

    def insert_day_columns(self):
        date = self.dataframe['_time']
        day = date.apply(lambda x: x.weekday())

        sinus_time = numpy.sin(2 * numpy.pi * day / DAYS_IN_WEEK)
        cosinus_time = numpy.cos(2 * numpy.pi * day / DAYS_IN_WEEK)

        self.dataframe.insert(1, 'sin_day', sinus_time)
        self.dataframe.insert(1, 'cos_day', cosinus_time)

    def insert_month_collumns(self):
        month = self.dataframe['_time'].dt.month

        sinus_time = numpy.sin(2 * numpy.pi * month / MONTHS_IN_YEAR)
        cosinus_time = numpy.cos(2 * numpy.pi * month / MONTHS_IN_YEAR)

        self.dataframe.insert(1, 'sin_month', sinus_time)
        self.dataframe.insert(1, 'cos_month', cosinus_time)

    def insert_season_collumns(self):
        season = self.get_seasons()

        return season / SEASONS_IN_YEAR

    def get_current_season(self):
        month = self.dataframe['_time'].dt.month
        day = self.dataframe['_time'].dt.day

        if (month == 3 & day >= 21) | (month in [4, 5]) | (month == 6 & day < 21):
            return 1#"SPRING"
        elif (month == 6 & day >= 21) | (month in [7, 8]) | (month == 9 & day < 23):
            return 2#"SUMMER"
        elif (month == 9 & day >= 23) | (month in [10, 11]) | (month == 12 & day < 21):
            return 3#"AUTUMN"
        else:
            return 4#"WINTER"

