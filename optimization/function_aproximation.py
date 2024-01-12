import math
import numpy as np
from scipy import optimize
import functools
import matplotlib.pyplot as plt


class FunctionAproximation:
    def __init__(self) -> None:
        pass

    def quadratic_binomial(self, x, a, b, c):
        if x is None:
            x = 0
        return a * x**2 + b * x + c

    def quadratic_aproximation(self, array):
        # starting with first pair
        x = []
        y = []

        for pair in array:
            x.append(pair[0])
            y.append(pair[1])
        x = np.array(x)
        y = np.array(y)

        optimal_params, cov_matrix = optimize.curve_fit(self.quadratic_binomial, x, y)
        ret_function = functools.partial(self.quadratic_binomial, a=optimal_params[0], b=optimal_params[1], c=optimal_params[2])
        return ret_function
