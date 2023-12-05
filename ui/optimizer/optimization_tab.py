import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QSlider, QLabel
from ui.optimizer.optimization_configs.hydro_configuration import HydroConfiguration
from ui.optimizer.optimization_configs.optimization_config import OptimizationConfiguration
from ui.optimizer.optimization_configs.solar_configuration import SolarConfiguration

from ui.optimizer.optimization_configs.thermal_coal_configuration import ThermalCoalConfiguration
from ui.optimizer.optimization_configs.thermal_gas_configuration import ThermalGasConfiguration
from ui.optimizer.optimization_configs.wind_configuration import WindConfiguration

class OptimizationTab():
    def __init__(self, tab: QWidget) -> None:
        #super(OptimizationTab, self).__init__()

        self.thermal_coal_tab = tab.findChild(QWidget, 'thermal_coal_tab')
        self.thermal_gas_tab = tab.findChild(QWidget, 'thermal_gas_tab')
        self.hydro_generator_tab = tab.findChild(QWidget, 'hydro_generator_tab')
        self.solar_generator_tab = tab.findChild(QWidget, 'solar_generator_tab')
        self.wind_generator_tab = tab.findChild(QWidget, 'wind_generator_tab')
        self.optimize_tab = tab.findChild(QWidget, 'optimize_tab')


        self.thermal_coal_config = ThermalCoalConfiguration(self.thermal_coal_tab)
        self.thermal_gas_config = ThermalGasConfiguration(self.thermal_gas_tab)
        self.hydro_config = HydroConfiguration(self.hydro_generator_tab)
        self.solar_config = SolarConfiguration(self.solar_generator_tab)
        self.wind_config = WindConfiguration(self.wind_generator_tab)
        self.optimization_config = OptimizationConfiguration(self.optimize_tab)