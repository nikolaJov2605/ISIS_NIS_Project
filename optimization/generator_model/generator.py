class Generator():
    def __init__(self, min_power_production, max_power_production, generator_type):
        self._min_power_production = min_power_production
        self._max_power_production = max_power_production
        self._generator_type = generator_type

    @property
    def min_power_production(self):
        return self._min_power_production

    @min_power_production.setter
    def min_power_production(self, value):
        self._min_power_production = value

    @property
    def max_power_production(self):
        return self._max_power_production

    @max_power_production.setter
    def max_power_production(self, value):
        self._max_power_production = value

    @property
    def generator_type(self):
        return self._generator_type

    @generator_type.setter
    def generator_type(self, value):
        self._generator_type = value
