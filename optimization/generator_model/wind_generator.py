from optimization.generator_model.generator import Generator


class WindGenerator(Generator):
    def __init__(self, min_power_production, max_power_production, generator_type, cut_in_speed, cut_out_speed, blade_length, efficiency):
        super().__init__(min_power_production, max_power_production, generator_type)
        self._cut_in_speed = cut_in_speed
        self._cut_out_speed = cut_out_speed
        self._blade_length = blade_length
        self._efficiency = efficiency

    @property
    def cut_in_speed(self):
        return self._cut_in_speed

    @cut_in_speed.setter
    def cut_in_speed(self, value):
        self._cut_in_speed = value

    @property
    def cut_out_speed(self):
        return self._cut_out_speed

    @cut_out_speed.setter
    def cut_out_speed(self, value):
        self._cut_out_speed = value

    @property
    def blade_length(self):
        return self._blade_length

    @blade_length.setter
    def blade_length(self, value):
        self._blade_length = value

    @property
    def efficiency(self):
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value):
        self._efficiency = value