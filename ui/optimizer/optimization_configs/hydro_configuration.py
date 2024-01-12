from PyQt5.QtWidgets import QWidget, QDoubleSpinBox

class HydroConfiguration:
    def __init__(self, tab: QWidget) -> None:
        self.hydro_cost_box = tab.findChild(QDoubleSpinBox, 'hydro_cost_box')
        self.hydro_co2_emission_box = tab.findChild(QDoubleSpinBox, 'hydro_co2_emission_box')

    def get_hydro_cost(self):
        return self.hydro_cost_box

    def get_hydro_co2_emission_box(self):
        return self.hydro_co2_emission_box