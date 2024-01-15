from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QPushButton
from matplotlib import pyplot as plt

from optimization.function_aproximation import FunctionAproximation

import numpy as np

from optimization.generator_model_loader.model_loader import GeneratorModelLoader

class ThermalCoalConfiguration():
    def __init__(self, tab) -> None:

        self.initialize_coal_consumption_elements(tab)
        self.initialize_coal_price_elements(tab)
        self.initialize_coal_co2_emission_elements(tab)

        self.update_lbl_values()

        self.slider_change_connections()

        self.aproximation = FunctionAproximation()


    def initialize_coal_consumption_elements(self, tab):
        self.coal_consumption_slider1 = tab.findChild(QSlider, 'coal_consumption_slider1')
        self.coal_consumption_slider2 = tab.findChild(QSlider, 'coal_consumption_slider2')
        self.coal_consumption_slider3 = tab.findChild(QSlider, 'coal_consumption_slider3')
        self.coal_consumption_slider4 = tab.findChild(QSlider, 'coal_consumption_slider4')
        self.coal_consumption_slider5 = tab.findChild(QSlider, 'coal_consumption_slider5')

        self.coal_consumption_slider_lbl1 = tab.findChild(QLabel, 'coal_consumption_slider_lbl1')
        self.coal_consumption_slider_lbl2 = tab.findChild(QLabel, 'coal_consumption_slider_lbl2')
        self.coal_consumption_slider_lbl3 = tab.findChild(QLabel, 'coal_consumption_slider_lbl3')
        self.coal_consumption_slider_lbl4 = tab.findChild(QLabel, 'coal_consumption_slider_lbl4')
        self.coal_consumption_slider_lbl5 = tab.findChild(QLabel, 'coal_consumption_slider_lbl5')

    def initialize_coal_price_elements(self, tab):
        self.coal_co2_cost_slider1 = tab.findChild(QSlider, 'coal_co2_cost_slider1')
        self.coal_co2_cost_slider2 = tab.findChild(QSlider, 'coal_co2_cost_slider2')
        self.coal_co2_cost_slider3 = tab.findChild(QSlider, 'coal_co2_cost_slider3')
        self.coal_co2_cost_slider4 = tab.findChild(QSlider, 'coal_co2_cost_slider4')
        self.coal_co2_cost_slider5 = tab.findChild(QSlider, 'coal_co2_cost_slider5')

        self.coal_price_slider_lbl1 = tab.findChild(QLabel, 'coal_price_slider_lbl1')
        self.coal_price_slider_lbl2 = tab.findChild(QLabel, 'coal_price_slider_lbl2')
        self.coal_price_slider_lbl3 = tab.findChild(QLabel, 'coal_price_slider_lbl3')
        self.coal_price_slider_lbl4 = tab.findChild(QLabel, 'coal_price_slider_lbl4')
        self.coal_price_slider_lbl5 = tab.findChild(QLabel, 'coal_price_slider_lbl5')

    def initialize_coal_co2_emission_elements(self, tab):
        self.coal_co2_emission_slider1 = tab.findChild(QSlider, 'coal_co2_emission_slider1')
        self.coal_co2_emission_slider2 = tab.findChild(QSlider, 'coal_co2_emission_slider2')
        self.coal_co2_emission_slider3 = tab.findChild(QSlider, 'coal_co2_emission_slider3')
        self.coal_co2_emission_slider4 = tab.findChild(QSlider, 'coal_co2_emission_slider4')
        self.coal_co2_emission_slider5 = tab.findChild(QSlider, 'coal_co2_emission_slider5')

        self.coal_co2_emission_slider_lbl1 = tab.findChild(QLabel, 'coal_co2_emission_slider_lbl1')
        self.coal_co2_emission_slider_lbl2 = tab.findChild(QLabel, 'coal_co2_emission_slider_lbl2')
        self.coal_co2_emission_slider_lbl3 = tab.findChild(QLabel, 'coal_co2_emission_slider_lbl3')
        self.coal_co2_emission_slider_lbl4 = tab.findChild(QLabel, 'coal_co2_emission_slider_lbl4')
        self.coal_co2_emission_slider_lbl5 = tab.findChild(QLabel, 'coal_co2_emission_slider_lbl5')

    # def initialize_buttons(self, tab: QWidget):
    #     self.aproximation_btn: QPushButton = tab.findChild(QPushButton, 'aproximation_btn')


    def slider_change_connections(self):
        self.coal_consumption_slider1.valueChanged.connect(self.update_lbl_values)
        self.coal_consumption_slider2.valueChanged.connect(self.update_lbl_values)
        self.coal_consumption_slider3.valueChanged.connect(self.update_lbl_values)
        self.coal_consumption_slider4.valueChanged.connect(self.update_lbl_values)
        self.coal_consumption_slider5.valueChanged.connect(self.update_lbl_values)

        self.coal_co2_cost_slider1.valueChanged.connect(self.update_lbl_values)
        self.coal_co2_cost_slider2.valueChanged.connect(self.update_lbl_values)
        self.coal_co2_cost_slider3.valueChanged.connect(self.update_lbl_values)
        self.coal_co2_cost_slider4.valueChanged.connect(self.update_lbl_values)
        self.coal_co2_cost_slider5.valueChanged.connect(self.update_lbl_values)

        self.coal_co2_emission_slider1.valueChanged.connect(self.update_lbl_values)
        self.coal_co2_emission_slider2.valueChanged.connect(self.update_lbl_values)
        self.coal_co2_emission_slider3.valueChanged.connect(self.update_lbl_values)
        self.coal_co2_emission_slider4.valueChanged.connect(self.update_lbl_values)
        self.coal_co2_emission_slider5.valueChanged.connect(self.update_lbl_values)

    # def button_connections(self):
    #     self.aproximation_btn.clicked.connect(self.do_aproximation)

    def do_aproximation(self):
        max_generator_power = GeneratorModelLoader.get_thermal_generator_coal().max_power_production
        x = [0, 0.2 * max_generator_power, 0.4 * max_generator_power, 0.6 * max_generator_power, 0.8 * max_generator_power, 1 * max_generator_power]
        y = [0]
        for val in self.return_co2_cost_values():
            y.append(val)
        #y = self.return_co2_cost_values()
        array = []
        for i in range(5):
            array.append((x[i], y[i]))


        ret_func = self.aproximation.quadratic_aproximation(array)

        plt.scatter(*zip(*array), label='Initial points')
        x_test = np.linspace(0, max_generator_power, 300)
        plt.plot(x_test, ret_func(x_test), 'r', label='Aproximation')


        plt.legend()
        plt.xlabel('P[MW]')
        plt.ylabel('c[$/MW]')
        plt.show()



    def update_lbl_values(self):
        self.coal_consumption_slider_lbl1.setText(str(self.coal_consumption_slider1.value()))
        self.coal_consumption_slider_lbl2.setText(str(self.coal_consumption_slider2.value()))
        self.coal_consumption_slider_lbl3.setText(str(self.coal_consumption_slider3.value()))
        self.coal_consumption_slider_lbl4.setText(str(self.coal_consumption_slider4.value()))
        self.coal_consumption_slider_lbl5.setText(str(self.coal_consumption_slider5.value()))

        self.coal_price_slider_lbl1.setText(str(self.coal_co2_cost_slider1.value()))
        self.coal_price_slider_lbl2.setText(str(self.coal_co2_cost_slider2.value()))
        self.coal_price_slider_lbl3.setText(str(self.coal_co2_cost_slider3.value()))
        self.coal_price_slider_lbl4.setText(str(self.coal_co2_cost_slider4.value()))
        self.coal_price_slider_lbl5.setText(str(self.coal_co2_cost_slider5.value()))

        self.coal_co2_emission_slider_lbl1.setText(str(self.coal_co2_emission_slider1.value()))
        self.coal_co2_emission_slider_lbl2.setText(str(self.coal_co2_emission_slider2.value()))
        self.coal_co2_emission_slider_lbl3.setText(str(self.coal_co2_emission_slider3.value()))
        self.coal_co2_emission_slider_lbl4.setText(str(self.coal_co2_emission_slider4.value()))
        self.coal_co2_emission_slider_lbl5.setText(str(self.coal_co2_emission_slider5.value()))

    def return_consumption_values(self):
        max_coal_consumption = GeneratorModelLoader.get_thermal_generator_coal().max_fuel_consumption
        return [
            self.coal_consumption_slider1.value() / 100,
            self.coal_consumption_slider2.value() / 100,
            self.coal_consumption_slider3.value() / 100,
            self.coal_consumption_slider4.value() / 100,
            self.coal_consumption_slider5.value() / 100
        ]

    def return_co2_cost_values(self):
        return [
            self.coal_co2_cost_slider1.value(),
            self.coal_co2_cost_slider2.value(),
            self.coal_co2_cost_slider3.value(),
            self.coal_co2_cost_slider4.value(),
            self.coal_co2_cost_slider5.value()
        ]

    def return_co2_emission_values(self):
        max_co2_emission = GeneratorModelLoader.get_thermal_generator_coal().max_fuel_co2_emission
        return [
            self.coal_co2_emission_slider1.value() / 100,
            self.coal_co2_emission_slider2.value() / 100,
            self.coal_co2_emission_slider3.value() / 100,
            self.coal_co2_emission_slider4.value() / 100,
            self.coal_co2_emission_slider5.value() / 100
        ]