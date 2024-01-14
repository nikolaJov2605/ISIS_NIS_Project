


import pandas
from database.database_manager import DatabaseManager
from optimization.function_aproximation import FunctionAproximation
from optimization.generator_model_loader.model_loader import GeneratorModelLoader
from optimization.power_calculation.solar_power_calculator import SolarPowerCalculator
from optimization.power_calculation.wind_power_calculation import WindPowerCalculation
from optimization.simplex import Simplex


class SimplexInvoker:
    def __init__(self, thermal_coal_generator_count, thermal_gas_generator_count, hydro_generator_count, wind_generator_count, solar_generator_count,
                 cost_weight_factor, co2_emission_weight_factor, coal_price_per_tone, gas_price_per_tone, optimization_date,
                 coal_counsumption_values, coal_co2_emission_values, coal_co2_cost_values,
                 gas_counsumption_values, gas_co2_emission_values, gas_co2_cost_values,
                 hydro_co2_emission_value, hydro_co2_cost_value) -> None:
        self.database_manager = DatabaseManager()
        self.function_aproximation = FunctionAproximation()
        self.load_models()

        self.thermal_coal_generator_count = thermal_coal_generator_count
        self.thermal_gas_generator_count = thermal_gas_generator_count
        self.hydro_generator_count = hydro_generator_count
        self.wind_generator_count = wind_generator_count
        self.solar_generator_count = solar_generator_count

        self.cost_weight_factor = cost_weight_factor / 100
        self.co2_emission_weight_factor = co2_emission_weight_factor / 100

        self.coal_price_per_tone = coal_price_per_tone
        self.gas_price_per_tone = gas_price_per_tone

        self.optimization_date = optimization_date

        self.coal_counsumption_values = coal_counsumption_values
        self.coal_co2_emission_values = coal_co2_emission_values
        self.coal_co2_cost_values = coal_co2_cost_values
        self.gas_counsumption_values = gas_counsumption_values
        self.gas_co2_emission_values = gas_co2_emission_values
        self.gas_co2_cost_values = gas_co2_cost_values
        self.hydro_co2_emission_value = hydro_co2_emission_value
        self.hydro_co2_cost_value = hydro_co2_cost_value

        wpc = WindPowerCalculation(self.wind_generator_count, self.optimization_date)
        self.wind_generator_hourly_load = wpc.calculate_hourly_power()

        spc = SolarPowerCalculator(self.solar_generator_count, self.optimization_date)
        self.solar_generator_hourly_load = spc.calculate_hourly_power()

        self.coal_generator_hourly_load = []
        self.gas_generator_hourly_load = []
        self.hydro_generator_hourly_load = []

        total_load_df = self.database_manager.read_from_database('Results')
        self.total_load = total_load_df['load'].tolist()

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



    def do_aproximation(self, function_values, max_generator_power):
        x = [0.2 * max_generator_power, 0.4 * max_generator_power, 0.6 * max_generator_power, 0.8 * max_generator_power, 1 * max_generator_power]
        y = function_values
        array = []
        for i in range(5):
            array.append((x[i], y[i]))


        ret_func = self.function_aproximation.quadratic_aproximation(array)
        return ret_func

    def start_optimization(self):
        self.coal_consumption_function = self.do_aproximation(self.coal_counsumption_values, GeneratorModelLoader.get_thermal_generator_coal().max_power_production)
        self.coal_co2_emission_function = self.do_aproximation(self.coal_co2_emission_values, GeneratorModelLoader.get_thermal_generator_coal().max_power_production)
        self.coal_co2_cost_function = self.do_aproximation(self.coal_co2_cost_values, GeneratorModelLoader.get_thermal_generator_coal().max_power_production)

        self.gas_consumption_function = self.do_aproximation(self.gas_counsumption_values, GeneratorModelLoader.get_thermal_generator_gas().max_power_production)
        self.gas_co2_emission_function = self.do_aproximation(self.gas_co2_emission_values, GeneratorModelLoader.get_thermal_generator_gas().max_power_production)
        self.gas_co2_cost_function = self.do_aproximation(self.gas_co2_cost_values, GeneratorModelLoader.get_thermal_generator_gas().max_power_production)

        self.hydro_co2_emission_const = self.hydro_co2_emission_value
        self.hydro_co2_cost_const = self.hydro_co2_cost_value

        simplex = Simplex()

        #loop
        for index, load in enumerate(self.total_load):
            hourly_target_load = load - self.wind_generator_hourly_load[index] - self.solar_generator_hourly_load[index]

            coal_hourly_power, gas_hourly_power, hydro_hourly_power = simplex.do_optimization(self.thermal_coal_generator_count, self.thermal_gas_generator_count, self.hydro_generator_count, self.wind_generator_count, self.solar_generator_count,
                    self.cost_weight_factor, self.co2_emission_weight_factor, self.coal_price_per_tone, self.gas_price_per_tone,
                    self.coal_consumption_function,self. coal_co2_emission_function, self.coal_co2_cost_function,
                    self.gas_consumption_function, self.gas_co2_emission_function, self.gas_co2_cost_function,
                    self.hydro_co2_emission_const, self.hydro_co2_cost_const,
                    hourly_target_load)
            self.coal_generator_hourly_load.append(coal_hourly_power)
            self.gas_generator_hourly_load.append(gas_hourly_power)
            self.hydro_generator_hourly_load.append(hydro_hourly_power)

    def load_optimization_report_load(self):
        ret_datarame = self.database_manager.read_from_database('Results')
        ret_datarame['coal_generator_load'] = self.coal_generator_hourly_load
        ret_datarame['gas_generator_load'] = self.gas_generator_hourly_load
        ret_datarame['hydro_generator_load'] = self.hydro_generator_hourly_load
        ret_datarame['wind_generator_load'] = self.wind_generator_hourly_load
        ret_datarame['solar_generator_load'] = self.solar_generator_hourly_load

        return ret_datarame
    
    def load_optimization_report_cost(self):
        ret_dataframe = pandas.DataFrame()
        coal_co2_cost = []
        gas_co2_cost = []
        hydro_co2_cost = []
        for load in self.coal_generator_hourly_load:
            coal_co2_cost.append(self.coal_co2_cost_function(load))
        for load in self.gas_generator_hourly_load:
            gas_co2_cost.append(self.gas_co2_cost_function(load))
        for load in self.hydro_generator_hourly_load:
            hydro_co2_cost.append(self.hydro_co2_cost_const)

        ret_dataframe['coal_generator_cost'] = coal_co2_cost
        ret_dataframe['gas_generator_cost'] = gas_co2_cost
        ret_dataframe['hydro_generator_cost'] = hydro_co2_cost

        return ret_dataframe
    
    def load_optimization_report_co2_emission(self):
        ret_dataframe = pandas.DataFrame()
        coal_co2_emission = []
        gas_co2_emission = []
        hydro_co2_emission = []

        for load in self.coal_generator_hourly_load:
            coal_co2_emission.append(self.coal_co2_emission_function(load))
        for load in self.gas_generator_hourly_load:
            gas_co2_emission.append(self.gas_co2_emission_function(load))
        for load in self.hydro_generator_hourly_load:
            hydro_co2_emission.append(self.hydro_co2_cost_const)

        ret_dataframe['coal_co2_emission'] = coal_co2_emission
        ret_dataframe['gas_co2_emission'] = gas_co2_emission
        ret_dataframe['hydro_co2_emission'] = hydro_co2_emission

        return ret_dataframe
    

        #plt.scatter(*zip(*array), label='Initial points')
        #x_test = np.linspace(0, 4, 300)
        #plt.plot(x_test, ret_func(x_test), 'r', label='Aproximation')


        # plt.legend()
        # plt.xlabel('P[MW]')
        # plt.ylabel('c[$/MW]')
        # plt.show()

