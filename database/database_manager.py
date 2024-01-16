import pyodbc as odbc
import urllib
import pandas
from sqlalchemy import create_engine
from datetime import datetime, timedelta

class DatabaseManager():
    def __init__(self):
        self.connection_string = "DRIVER={ODBC Driver 17 for SQL Server};Server=DESKTOP-1TFLJCH;Database=LoadPredictionDatabase;Trusted_Connection=yes;"
        quoted = urllib.parse.quote_plus(self.connection_string)
        self.engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))


    def write_to_database(self, data_frame, table_name):
        try:
            data_frame.to_sql(name=table_name, index=False, con = self.engine, if_exists='replace')
            return True
        except:
            print("An exception occurred during storing data to database")
            return False


    def read_from_database(self, table_name):
        df = pandas.read_sql_table(table_name, self.engine)

        return df


    def read_measures_from_database_by_time(self, starting_time, ending_time):
        #ending_time = datetime.strptime(ending_time, '%Y-%m-%d')
        starting_time = starting_time.strftime('%Y-%m-%d')
        ending_time = ending_time + timedelta(days=1)
        ending_time = ending_time.strftime('%Y-%m-%d')
        params = [starting_time, ending_time]
        query = "SELECT * from Measures WHERE _time >= '{param0}' and _time < '{param1}'".format(param0=params[0], param1=params[1])

        df = pandas.read_sql_query(query, con=self.engine)
        return df

    def read_testing_measures_from_database_by_time(self, starting_time, ending_time):
        #ending_time = datetime.strptime(ending_time, '%Y-%m-%d')
        starting_time = starting_time.strftime('%Y-%m-%d')
        ending_time = ending_time + timedelta(days=1)
        ending_time = ending_time.strftime('%Y-%m-%d')
        params = [starting_time, ending_time]
        query = "SELECT * from TestMeasures WHERE _time >= '{param0}' and _time < '{param1}'".format(param0=params[0], param1=params[1])

        df = pandas.read_sql_query(query, con=self.engine)
        return df

    def read_results_from_database_by_time(self, starting_time, ending_time):
        #ending_time = datetime.strptime(ending_time, '%Y-%m-%d')
        starting_time = starting_time.strftime('%Y-%m-%d')
        ending_time = ending_time + timedelta(days=1)
        ending_time = ending_time.strftime('%Y-%m-%d')
        params = [starting_time, ending_time]
        query = "SELECT * from Results WHERE _time >= '{param0}' and _time < '{param1}'".format(param0=params[0], param1=params[1])

        df = pandas.read_sql_query(query, con=self.engine)
        return df

    def read_solar_radiation_from_database_by_time(self, starting_time, ending_time):
        starting_time = starting_time.strftime('%Y-%m-%d')
        ending_time = ending_time + timedelta(days=1)
        ending_time = ending_time.strftime('%Y-%m-%d')
        params = [starting_time, ending_time]
        query = "SELECT * from SolarRadiation WHERE time >= '{param0}' and time < '{param1}'".format(param0=params[0], param1=params[1])

        df = pandas.read_sql_query(query, con=self.engine)
        return df


