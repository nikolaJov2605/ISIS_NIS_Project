from optimization.generator_model_loader.model_loader import GeneratorModelLoader
from pulp import *
class Simplex():
    def __init__(self) -> None:
        pass

    def do_optimization(self, thermal_coal_generator_count, thermal_gas_generator_count, hydro_generator_count, wind_generator_count, solar_generator_count,
                 cost_weight_factor, co2_emission_weight_factor, coal_price_per_tone, gas_price_per_tone,
                 coal_consumption_function, coal_co2_emission_function, coal_co2_cost_function,
                 gas_consumption_function, gas_co2_emission_function, gas_co2_cost_function,
                 hydro_co2_emission_const, hydro_co2_cost_const,
                 target_load):

        coal_low_boundary = GeneratorModelLoader.get_thermal_generator_coal().min_power_production * thermal_coal_generator_count
        coal_high_boundary = GeneratorModelLoader.get_thermal_generator_coal().max_power_production * thermal_coal_generator_count

        gas_low_boundary = GeneratorModelLoader.get_thermal_generator_gas().min_power_production * thermal_gas_generator_count
        gas_high_boundary = GeneratorModelLoader.get_thermal_generator_gas().max_power_production * thermal_gas_generator_count

        hydro_low_boundary = GeneratorModelLoader.get_hydro_generator().min_power_production * hydro_generator_count
        hydro_high_boundary = GeneratorModelLoader.get_hydro_generator().max_power_production * hydro_generator_count

        # coal
        x0 = LpVariable("x_coal", coal_low_boundary, coal_high_boundary)
        # gas
        x1 = LpVariable("x_gas", gas_low_boundary, gas_high_boundary)
        # hydro
        x2 = LpVariable("x_hydro", hydro_low_boundary, hydro_high_boundary)

        #objective = cost_weight_factor * (cost_function_coal(x_coal) + cost_function_gas(x_gas) + cost_function_hydro(x_hydro)) + \
        #    co2_emission_weight_factor * (co2_function_coal(x_coal) + co2_function_gas(x_gas))

        objective_function = (cost_weight_factor * (coal_consumption_function(x0.varValue) * coal_price_per_tone + coal_co2_cost_function(x0.varValue)) \
                        + co2_emission_weight_factor * (coal_co2_emission_function(x0.varValue))) * x0 \
                        + (cost_weight_factor * (gas_consumption_function(x1.varValue) * gas_price_per_tone + gas_co2_cost_function(x1.varValue)) \
                        + co2_emission_weight_factor * (gas_co2_emission_function(x1.varValue))) * x1 \
                        + (cost_weight_factor * hydro_co2_cost_const \
                        + co2_emission_weight_factor * hydro_co2_emission_const) * x2

        #constraint = x0 + x1 + x2 == target_load ovo moze u invokeru da se odradi pa da se kroz loop poziva optimizacija za svaki sat
        constraint = x0 + x1 + x2 == target_load

        #prob = LpProblem("Power_Optimization", LpMinimize)
        problem = LpProblem("Power_Load_Optimization", LpMinimize)

        problem += objective_function
        problem += constraint

        problem.solve()

        optimal_power_coal = value(x0)
        optimal_power_gas = value(x1)
        optimal_power_hydro = value(x2)

        # Print or use the optimal values as needed
        print("Optimal Power from Coal: ", optimal_power_coal)
        print("Optimal Power from Gas: ", optimal_power_gas)
        print("Optimal Power from Hydro: ", optimal_power_hydro)
        print("Target Power Load:", target_load)

        return optimal_power_coal, optimal_power_gas, optimal_power_hydro