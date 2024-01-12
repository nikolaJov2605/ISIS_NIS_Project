from PyQt5.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox, QPushButton

MAX_PERCENTAGE = 100

class OptimizationConfiguration:
    def __init__(self, tab: QWidget) -> None:
        self.init_generator_counts(tab)
        self.init_optimization_weight_factors(tab)
        self.init_fuel_prices(tab)
        self.initialize_buttons(tab)

        self.button_click_connections()
        self.optimization_weight_factors_changed_connections()


    def init_generator_counts(self, tab: QWidget):
        self.coal_generator_cnt_box: QSpinBox = tab.findChild(QSpinBox, 'coal_generator_cnt_box')
        self.gas_generator_cnt_box: QSpinBox = tab.findChild(QSpinBox, 'gas_generator_cnt_box')
        self.hydro_generator_cnt_box: QSpinBox = tab.findChild(QSpinBox, 'hydro_generator_cnt_box')
        self.solar_generator_cnt_box: QSpinBox = tab.findChild(QSpinBox, 'solar_generator_cnt_box')
        self.wind_generator_cnt_box: QSpinBox = tab.findChild(QSpinBox, 'wind_generator_cnt_box')

    def init_optimization_weight_factors(self, tab: QWidget):
        self.cost_optimization_percent_box: QSpinBox = tab.findChild(QSpinBox, 'cost_optimization_percent_box')
        self.co2_emission_optimization_percent_box: QSpinBox = tab.findChild(QSpinBox, 'co2_emission_optimization_percent_box')


    def init_fuel_prices(self, tab: QWidget):
        self.coal_price_box: QDoubleSpinBox = tab.findChild(QDoubleSpinBox, 'coal_price_box')
        self.gas_price_box: QDoubleSpinBox = tab.findChild(QDoubleSpinBox, 'gas_price_box')

    def initialize_buttons(self, tab: QWidget):
        self.optimize_by_cost_btn: QPushButton = tab.findChild(QPushButton, 'optimize_by_cost_btn')
        self.co2_optimization_percent_box: QPushButton = tab.findChild(QPushButton, 'co2_optimization_percent_box')



    def button_click_connections(self):
        self.optimize_by_cost_btn.clicked.connect(self.set_max_factor_for_cost_optimization)
        self.co2_optimization_percent_box.clicked.connect(self.set_max_factor_for_co2_emission_optimization)

    def optimization_weight_factors_changed_connections(self):
        self.co2_emission_optimization_percent_box.valueChanged.connect(self.calculate_new_cost_factor)
        self.cost_optimization_percent_box.valueChanged.connect(self.calculate_new_co2_emission_factor)



    def calculate_new_cost_factor(self):
        self.cost_optimization_percent_box.setValue(MAX_PERCENTAGE - self.co2_emission_optimization_percent_box.value())

    def calculate_new_co2_emission_factor(self):
            self.co2_emission_optimization_percent_box.setValue(MAX_PERCENTAGE - self.cost_optimization_percent_box.value())

    def set_max_factor_for_cost_optimization(self):
        self.cost_optimization_percent_box.setValue(self.cost_optimization_percent_box.maximum())
        self.co2_emission_optimization_percent_box.setValue(self.co2_emission_optimization_percent_box.minimum())

    def set_max_factor_for_co2_emission_optimization(self):
        self.co2_emission_optimization_percent_box.setValue(self.co2_emission_optimization_percent_box.maximum())
        self.cost_optimization_percent_box.setValue(self.cost_optimization_percent_box.minimum())