import numpy

from database.database_manager import DatabaseManager


class DataHelper:
    def __init__(self) -> None:
        self.database_manager = DatabaseManager()

    def create_dataset(self, dataset, look_back):
        dataX, dataY = [], []
        for i in range(len(dataset)):
            a = dataset[i, 0:look_back-1]
            dataX.append(a)
            dataY.append(dataset[i, look_back-1])
        return numpy.array(dataX), numpy.array(dataY)


    def load_data_from_database(self, starting_time, ending_time):
        self.database_manager = DatabaseManager()
        dataframe = self.database_manager.read_measures_from_database_by_time(starting_time, ending_time)
        del dataframe['_time']
        #dataframe.to_csv('db_measures.csv', index=False)
        return dataframe

