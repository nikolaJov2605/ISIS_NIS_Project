from optimization.generator_model.generator import Generator


class SolarGenerator(Generator):
    def __init__(self, min_power_production, max_power_production, efficiency, sum_panel_size, generator_type):
        super().__init__(min_power_production, max_power_production, generator_type)
        self._efficiency = efficiency
        self._sum_panel_size = sum_panel_size

    @property
    def efficiency(self):
        return self._efficiency

    @efficiency.setter
    def cut_in_speed(self, value):
        self._efficiency = value

    @property
    def sum_panel_size(self):
        return self._sum_panel_size

    @efficiency.setter
    def sum_panel_size(self, value):
        self._sum_panel_size = value