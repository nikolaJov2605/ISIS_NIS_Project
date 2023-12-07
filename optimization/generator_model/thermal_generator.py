from optimization.generator_model.generator import Generator


class ThermalGenerator(Generator):
    def __init__(self, min_power_production, max_power_production, generator_type, max_fuel_consumption, max_co2_emission):
        super().__init__(min_power_production, max_power_production, generator_type)
        self._max_fuel_consumption = max_fuel_consumption
        self._max_co2_emission = max_co2_emission

    @property
    def max_fuel_consumption(self):
        return self._max_fuel_consumption

    @max_fuel_consumption.setter
    def max_max_fuel_consumption(self, value):
        self._max_fuel_consumption = value

    @property
    def max_fuel_co2_emission(self):
        return self._max_fuel_consumption

    @max_fuel_co2_emission.setter
    def max_fuel_co2_emission(self, value):
        self._max_fuel_co2_emission = value