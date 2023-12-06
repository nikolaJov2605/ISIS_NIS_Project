import json

from optimization.generator_model.generator_type import GeneratorType
from optimization.generator_model.hydro_generator import HydroGenerator
from optimization.generator_model.solar_generator import SolarGenerator
from optimization.generator_model.thermal_generator import ThermalGenerator
from optimization.generator_model.wind_generator import WindGenerator


class GeneratorModelLoader():

    def __init__(self) -> None:
        self.thermal_generator_coal = None
        self.thermal_generator_gas = None
        self.hydro_generator = None
        self.solar_genereator = None
        self.wind_generator = None
        self.load_generator_models()

    @property
    def get_thermal_generator_coal(self):
        return self.thermal_generator_coal

    @property
    def get_thermal_generator_gas(self):
        return self.thermal_generator_gas

    @property
    def get_hydro_generator(self):
        return self.hydro_generator

    @property
    def get_solar_generator(self):
        return self.solar_genereator

    @property
    def get_wind_generator(self):
        return self.wind_generator

    def load_generator_models(self):
        coal_gen_params = self.load_generators_from_json('D:/Fakultet/Master/Inteligentni softverski infrastrukturni sistemi/Projekat/ISIS_NIS_Project/optimization/generator_model_loader/json_model/thermal_generator_coal.json')
        self.thermal_generator_coal = ThermalGenerator(**coal_gen_params)
        gas_gen_params = self.load_generators_from_json('D:/Fakultet/Master/Inteligentni softverski infrastrukturni sistemi/Projekat/ISIS_NIS_Project/optimization/generator_model_loader/json_model/thermal_generator_gas.json')
        self.thermal_generator_gas = ThermalGenerator(**gas_gen_params)
        hydro_params = self.load_generators_from_json('D:/Fakultet/Master/Inteligentni softverski infrastrukturni sistemi/Projekat/ISIS_NIS_Project/optimization/generator_model_loader/json_model/hydro_generator.json')
        self.hydro_generator = HydroGenerator(**hydro_params)
        solar_params = self.load_generators_from_json('D:/Fakultet/Master/Inteligentni softverski infrastrukturni sistemi/Projekat/ISIS_NIS_Project/optimization/generator_model_loader/json_model/solar_generator.json')
        self.solar_genereator = SolarGenerator(**solar_params)
        wind_params = self.load_generators_from_json('D:/Fakultet/Master/Inteligentni softverski infrastrukturni sistemi/Projekat/ISIS_NIS_Project/optimization/generator_model_loader/json_model/wind_generator.json')
        self.wind_generator = WindGenerator(**wind_params)


    def load_generators_from_json(self, filename):
        json_object = {}
        with open(filename, 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)

        json_object['generator_type'] = GeneratorType(json_object['generator_type'])

        return json_object