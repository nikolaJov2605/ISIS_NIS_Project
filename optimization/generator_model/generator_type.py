from enum import Enum


class GeneratorType(int, Enum):
    THERMAL_GENERATOR_COAL = 1
    THERMAL_GENERATOR_GAS = 2
    HYDRO_GENERATOR = 3
    SOLAR_GENERATOR = 4
    WIND_GENERATOR = 5