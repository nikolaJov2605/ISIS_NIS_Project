from PyQt5.QtWidgets import QWidget, QDoubleSpinBox

class HydroConfiguration:
    def __init__(self, tab: QWidget) -> None:
        self.hydro_cost_box = tab.findChild(QDoubleSpinBox, 'hydro_cost_box')

    def get_hydro_cost(self):
        return self.hydro_cost_box