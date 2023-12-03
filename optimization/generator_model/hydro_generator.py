from optimization.generator_model.generator import Generator


class HydroGenerator(Generator):
    def __init__(self, min_power_production, max_power_production, generator_type):
        super().__init__(min_power_production, max_power_production, generator_type)