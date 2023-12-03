from optimization.generator_model.generator import Generator


class ThermalGenerator(Generator):
    def __init__(self, min_power_production, max_power_production, generator_type, fuel_consumption, co2_emission):
        super().__init__(min_power_production, max_power_production, generator_type)
        self._fuel_consumption = fuel_consumption
        self._co2_emission = co2_emission

    @property
    def fuel_consumption(self):
        return self._fuel_consumption

    @fuel_consumption.setter
    def fuel_consumption(self, value):
        self._fuel_consumption = value

    @property
    def fuel_co2_emission(self):
        return self._fuel_consumption

    @fuel_co2_emission.setter
    def fuel_co2_emission(self, value):
        self._fuel_co2_emission = value