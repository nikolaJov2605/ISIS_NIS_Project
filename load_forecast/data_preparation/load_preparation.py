import pandas


LOAD_COLS = ["DateShort", "TimeFrom", "TimeTo", "Load (MW/h)"]

class LoadPreparer():
    def reorder_load_data(self, data_frame):
        data_frame["DateShort"] = data_frame['DateShort'].astype(str) + " " + data_frame["TimeFrom"].astype(str)
        data_frame['DateShort'] = pandas.to_datetime(data_frame['DateShort'], yearfirst=True)
        #data_frame.drop(['TimeFrom', 'TimeTo'], axis=1)
        del data_frame['TimeFrom']
        del data_frame['TimeTo']
        data_frame.rename(columns={'Load (MW/h)':'load'}, inplace=True)
        data_frame.rename(columns={'DateShort':'_time'}, inplace=True)

        return data_frame