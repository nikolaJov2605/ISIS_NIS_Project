import pyodbc as odbc
import urllib
import pandas
from sqlalchemy import create_engine

class DatabaseManager():
    def __init__(self):
        self.connection_string = "DRIVER={ODBC Driver 17 for SQL Server};Server=DESKTOP-1TFLJCH;Database=LoadPredictionDatabase;Trusted_Connection=yes;"
        quoted = urllib.parse.quote_plus(self.connection_string)
        self.engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
        #self.connection = odbc.connect(self.connection_string)
        #self.cursor = self.connection.cursor()

    def write_to_database(self, data_frame):
        try:
            data_frame.to_sql(name='Measures', index=False, con = self.engine, if_exists='replace')
            return True
        except:
            print("An exception occurred during storing data to database")
            return False


    def read_from_database(self):
        df = pandas.read_sql_table("Measures", self.engine)

        return df


    def read_from_database_by_time(self, starting_time, ending_time):
        params = [starting_time, ending_time]
        query = "SELECT * from Measures WHERE _time >= '{param0}' and _time <= '{param1}'".format(param0=params[0], param1=params[1])

        df = pandas.read_sql_query(query, con=self.engine)
        return df


