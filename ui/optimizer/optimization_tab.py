import pandas
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from ui.optimizer.optimization_configs.hydro_configuration import HydroConfiguration
from ui.optimizer.optimization_configs.optimization_config import OptimizationConfiguration
from ui.optimizer.optimization_configs.solar_configuration import SolarConfiguration

from ui.optimizer.optimization_configs.thermal_coal_configuration import ThermalCoalConfiguration
from ui.optimizer.optimization_configs.thermal_gas_configuration import ThermalGasConfiguration
from ui.optimizer.optimization_configs.wind_configuration import WindConfiguration

class OptimizationTab():
    def __init__(self, tab: QWidget) -> None:
        #super(OptimizationTab, self).__init__()
        self.tab = tab

        self.init_config_tabs()
        self.init_report_tables()


        self.thermal_coal_config = ThermalCoalConfiguration(self.thermal_coal_tab)
        self.thermal_gas_config = ThermalGasConfiguration(self.thermal_gas_tab)
        self.hydro_config = HydroConfiguration(self.hydro_generator_tab)
        self.solar_config = SolarConfiguration(self.solar_generator_tab)
        self.wind_config = WindConfiguration(self.wind_generator_tab)
        self.optimization_config = OptimizationConfiguration(self.optimize_tab)







    def init_config_tabs(self):
        self.thermal_coal_tab = self.tab.findChild(QWidget, 'thermal_coal_tab')
        self.thermal_gas_tab = self.tab.findChild(QWidget, 'thermal_gas_tab')
        self.hydro_generator_tab = self.tab.findChild(QWidget, 'hydro_generator_tab')
        self.solar_generator_tab = self.tab.findChild(QWidget, 'solar_generator_tab')
        self.wind_generator_tab = self.tab.findChild(QWidget, 'wind_generator_tab')
        self.optimize_tab = self.tab.findChild(QWidget, 'optimize_tab')

    def init_report_tables(self):
        self.daily_load_report_table = self.tab.findChild(QTableWidget, 'daily_load_report_table')
        self.thermal_coal_report_table = self.tab.findChild(QTableWidget, 'thermal_coal_report_table')
        self.thermal_gas_report_table = self.tab.findChild(QTableWidget, 'thermal_gas_report_table')
        self.hydro_report_table = self.tab.findChild(QTableWidget, 'hydro_report_table')
        self.solar_report_table = self.tab.findChild(QTableWidget, 'solar_report_table')
        self.wind_report_table = self.tab.findChild(QTableWidget, 'wind_report_table')



    def populate_table(self, table_name, data_frame):
        table = self.tab.findChild(QTableWidget, table_name)
        table.setRowCount(data_frame.shape[0])
        table.setColumnCount(data_frame.shape[1])

        table.setHorizontalHeaderLabels(list(data_frame.columns))

        for i in range(data_frame.shape[0]):
            for j in range(data_frame.shape[1]):
                item = QTableWidgetItem(str(data_frame.iloc[i, j]))
                item.setTextAlignment(Qt.AlignHCenter)
                table.setItem(i, j, item)

        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def calculate_daily_load(self):
        daily_load_df = self.convert_table_to_dataframe(self.daily_load_report_table)

        daily_load_df['load'] = daily_load_df['load'].astype(float)
        daily_sum = daily_load_df['load'].sum()
        self.load_sum_lbl: QLabel = self.tab.findChild(QLabel, 'load_sum_lbl')
        self.load_sum_lbl.setText(str(daily_sum))

       # return daily_load_df['load'].sum()


    def convert_table_to_dataframe(self, table: QTableWidget):
        rows = table.rowCount()
        cols = table.columnCount()

        # Extract headers
        headers = [table.horizontalHeaderItem(col).text() for col in range(cols)]

        data = []

        for row in range(rows):
            row_data = [table.item(row, col).text() for col in range(cols)]
            data.append(row_data)

        df = pandas.DataFrame(data, columns=headers)
        return df