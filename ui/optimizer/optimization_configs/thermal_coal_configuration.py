from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QSlider, QLabel

class ThermalCoalConfiguration():
    def __init__(self, tab) -> None:

        self.initialize_coal_consumption_elements(tab)
        self.initialize_coal_price_elements(tab)
        self.initialize_coal_co2_emission_elements(tab)

        self.update_lbl_values()

        self.slider_change_connections()


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
        return [
            self.coal_consumption_slider1.value(),
            self.coal_consumption_slider2.value(),
            self.coal_consumption_slider3.value(),
            self.coal_consumption_slider4.value(),
            self.coal_consumption_slider5.value()
        ]

    def return_price_values(self):
        return [
            self.coal_co2_cost_slider1.value(),
            self.coal_co2_cost_slider2.value(),
            self.coal_co2_cost_slider3.value(),
            self.coal_co2_cost_slider4.value(),
            self.coal_co2_cost_slider5.value()
        ]

    def return_co2_emission_values(self):
        return [
            self.coal_co2_emission_slider1.value(),
            self.coal_co2_emission_slider2.value(),
            self.coal_co2_emission_slider3.value(),
            self.coal_co2_emission_slider4.value(),
            self.coal_co2_emission_slider5.value()
        ]