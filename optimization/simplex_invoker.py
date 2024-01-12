


from database.database_manager import DatabaseManager
from optimization.generator_model_loader.model_loader import GeneratorModelLoader
from optimization.power_calculation.solar_power_calculator import SolarPowerCalculator
from optimization.power_calculation.wind_power_calculation import WindPowerCalculation


class SimplexInvoker:
    def __init__(self, thermal_coal_generator_count, thermal_gas_generator_count, hydro_generator_count, wind_generator_count, solar_generator_count,
                 cost_weight_factor, co2_emission_weight_factor, coal_price_per_tone, gas_price_per_tone, optimization_date) -> None:
        self.database_manager = DatabaseManager()
        self.load_models()

        self.thermal_coal_generator_count = thermal_coal_generator_count
        self.thermal_gas_generator_count = thermal_gas_generator_count
        self.hydro_generator_count = hydro_generator_count
        self.wind_generator_count = wind_generator_count
        self.solar_generator_count = solar_generator_count

        self.cost_weight_factor = cost_weight_factor
        self.co2_emission_weight_factor = co2_emission_weight_factor

        self.coal_price_per_tone = coal_price_per_tone
        self.gas_price_per_tone = gas_price_per_tone

        self.optimization_date = optimization_date

        wpc = WindPowerCalculation(self.wind_generator_count, self.optimization_date)
        self.wind_generator_hourly_load = wpc.calculate_hourly_power()

        spc = SolarPowerCalculator(self.solar_generator_count, self.optimization_date)
        self.solar_generator_hourly_load = spc.calculate_hourly_power()

        self.total_load = self.database_manager.read_from_database('Results')

        print('\nSOLAR_HOURLY_LOAD: ')
        print(self.solar_generator_hourly_load)
        print('\nWIND_HOURLY_LOAD: ')
        print(self.wind_generator_hourly_load)



    def load_models(self):
        self.thermal_coal_powerplant = GeneratorModelLoader.get_thermal_generator_coal()
        self.thermal_gas_powerplant = GeneratorModelLoader.get_thermal_generator_gas()
        self.hydro_powerplant = GeneratorModelLoader.get_hydro_generator()
        self.wind_powerplant = GeneratorModelLoader.get_wind_generator()
        self.solar_powerplant = GeneratorModelLoader.get_solar_generator()



    # def load_function_aproximations(self):



    # povuci sve potrebne informacije sa UI-a
    #   - svi modeli generatora
    #   - aproksimacije funkcija definisanih dijagramima
    #       - coal consumption
    #       - coal CO2 emission
    #       - coal CO2 price per tone
    #       - gas consumption
    #       - gas CO2 emission
    #       - gas CO2 price per tone
    #       - hydro cost
    #       - hydro CO2 emission cost
    #   - broj elektrana na ugalj   #
    #   - broj elektrana na gas     #
    #   - broj hidroelektrana       #
    #   - broj solarnih elektrana   #
    #   - broj vetroelektrana       #
    #
    #   - tezinski faktor za cost   #
    #   - tezinski faktor za co2    #
    #
    #   - cena uglja                #
    #   - cena gasa                 #
    #
    #   - ucitati iz baze potrosnju za 24 sata
    #   - ucitati i proracun solarnih i vetroelektrana  #
    #
    #