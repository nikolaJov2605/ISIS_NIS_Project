from matplotlib import pyplot as plt
import pandas
import numpy
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
from optimization.simplex_invoker import SimplexInvoker
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
        self.optimization_date = None

        self.init_config_tabs()
        self.init_report_tables()
        self.init_buttons()


        self.thermal_coal_config = ThermalCoalConfiguration(self.thermal_coal_tab)
        self.thermal_gas_config = ThermalGasConfiguration(self.thermal_gas_tab)
        self.hydro_config = HydroConfiguration(self.hydro_generator_tab)
        self.solar_config = SolarConfiguration(self.solar_generator_tab)
        self.wind_config = WindConfiguration(self.wind_generator_tab)
        self.optimization_config = OptimizationConfiguration(self.optimize_tab)

        # optimization trigger
        self.optimization_btn.clicked.connect(self.optimize)







    def init_config_tabs(self):
        self.thermal_coal_tab = self.tab.findChild(QWidget, 'thermal_coal_tab')
        self.thermal_gas_tab = self.tab.findChild(QWidget, 'thermal_gas_tab')
        self.hydro_generator_tab = self.tab.findChild(QWidget, 'hydro_generator_tab')
        self.solar_generator_tab = self.tab.findChild(QWidget, 'solar_generator_tab')
        self.wind_generator_tab = self.tab.findChild(QWidget, 'wind_generator_tab')
        self.optimize_tab = self.tab.findChild(QWidget, 'optimize_tab')

    def init_report_tables(self):
        self.daily_load_report_table = self.tab.findChild(QTableWidget, 'daily_load_report_table')
        self.load_report_table = self.tab.findChild(QTableWidget, 'load_report_table')
        self.cost_report_table = self.tab.findChild(QTableWidget, 'cost_report_table')
        self.co2_emission_report_table = self.tab.findChild(QTableWidget, 'co2_emission_report_table')

    def init_buttons(self):
        self.optimization_btn = self.tab.findChild(QPushButton, 'optimization_btn')



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


    def plot_dataframe(self, dataframe):
        load_contribution_df = dataframe.drop(columns=['_time', 'load']).cumsum(axis=1)

        plt.figure(figsize=(10, 6))

        # Plotting the target load as a reference
        plt.plot(dataframe['_time'], dataframe['load'], label='Target Load', linestyle='--', color='black', marker='o')

        # hydro
        plt.fill_between(dataframe['_time'], 0, dataframe['hydro'], label='Hydro Generator', alpha=0.7, color="blue")
        # coal
        plt.fill_between(dataframe['_time'], dataframe['hydro'], dataframe['hydro'] + dataframe['coal'], label='Coal Generator', alpha=0.7, color="brown")
        # gas
        plt.fill_between(dataframe['_time'], dataframe['hydro'] + dataframe['coal'],
                        dataframe['hydro'] + dataframe['coal'] + dataframe['gas'], label='Gas Generator', alpha=0.7, color="gray")
        # wind
        plt.fill_between(dataframe['_time'], dataframe['hydro'] + dataframe['coal'] + dataframe['gas'],
                        dataframe['hydro'] + dataframe['coal'] + dataframe['gas'] + dataframe['wind'],
                        label='Wind Generator', alpha=0.7, color="green")
        # solar
        plt.fill_between(dataframe['_time'], dataframe['hydro'] + dataframe['coal'] + dataframe['gas'] + dataframe['wind'],
                        dataframe['hydro'] + dataframe['coal'] + dataframe['gas'] + dataframe['wind'] + dataframe['solar'],
                        label='Solar Generator', alpha=0.7, color="yellow")
        # missing
        plt.fill_between(dataframe['_time'], dataframe['hydro'] + dataframe['coal'] + dataframe['gas'] + dataframe['wind'] + dataframe['solar'],
                        dataframe['hydro'] + dataframe['coal'] + dataframe['gas'] + dataframe['wind'] + dataframe['solar'] + dataframe['missing'],
                        label='Missing Load', alpha=0.7, color="red")


        # Adding labels and title
        plt.xlabel('Hour of the Day')
        plt.ylabel('Load (MW)')
        plt.title('Hourly Generator Loads')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)

        # Show the plot
        plt.tight_layout()
        plt.show()


    def optimize(self):
        thermal_coal_generator_count = self.optimization_config.coal_generator_cnt_box.value()
        thermal_gas_generator_count = self.optimization_config.gas_generator_cnt_box.value()
        hydro_generator_count = self.optimization_config.hydro_generator_cnt_box.value()
        solar_generator_count = self.optimization_config.solar_generator_cnt_box.value()
        wind_generator_count = self.optimization_config.wind_generator_cnt_box.value()

        cost_weight_factor = self.optimization_config.cost_optimization_percent_box.value()
        co2_emission_weight_factor = self.optimization_config.co2_emission_optimization_percent_box.value()

        coal_price_per_tone = self.optimization_config.coal_price_box.value()
        gas_price_per_tone = self.optimization_config.gas_price_box.value()

        optimization_date = self.optimization_date

        coal_counsumption_values = self.thermal_coal_config.return_consumption_values()
        coal_co2_emission_values = self.thermal_coal_config.return_co2_emission_values()
        coal_co2_cost_values = self.thermal_coal_config.return_co2_cost_values()

        gas_counsumption_values = self.thermal_gas_config.return_consumption_values()
        gas_co2_emission_values = self.thermal_gas_config.return_co2_emission_values()
        gas_co2_cost_values = self.thermal_gas_config.return_co2_cost_values()

        hydro_co2_emission_value = self.hydro_config.get_hydro_co2_emission()
        hydro_co2_cost_value = self.hydro_config.get_hydro_cost()


        if optimization_date == None:
            return

        simplex_invoker = SimplexInvoker(thermal_coal_generator_count, thermal_gas_generator_count, hydro_generator_count, wind_generator_count, solar_generator_count,
                                         cost_weight_factor, co2_emission_weight_factor, coal_price_per_tone, gas_price_per_tone, optimization_date,
                                         coal_counsumption_values, coal_co2_emission_values, coal_co2_cost_values, gas_counsumption_values, gas_co2_emission_values, gas_co2_cost_values,
                                         hydro_co2_emission_value, hydro_co2_cost_value)

        simplex_invoker.start_optimization()

        report_data_load = simplex_invoker.load_optimization_report_load()
        report_data_co2_cost = simplex_invoker.load_optimization_report_cost()
        report_data_co2_emission = simplex_invoker.load_optimization_report_co2_emission()

        self.populate_table('load_report_table', report_data_load)
        self.populate_table('cost_report_table', report_data_co2_cost)
        self.populate_table('co2_emission_report_table', report_data_co2_emission)

        self.plot_dataframe(report_data_load)

        return