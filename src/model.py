from sympy import symbols, sympify, lambdify, solve
import numpy as np
from scipy.optimize import fsolve

class FunctionModel:
    def __init__(self):
        self.x = symbols('x')
        self.fx = None       
        self.gx = None         

    def set_fx(self, expression):
        self.fx = self._parse_function(expression)

    def set_gx(self, expression):
        self.gx = self._parse_function(expression)

    def evaluate(self, func, x_values):
        if func is None:
            return None
        try:
            x_vals = np.array(x_values)
            func_lambda = lambdify(self.x, func, "numpy")
            return func_lambda(x_vals)
        except Exception as e:
            print(f"Error evaluating function: {e}")
            return None

    def _parse_function(self, expression):
        try:
            expression = expression.replace('^', '**')
            return sympify(expression, evaluate=False)
        except Exception as e:
            print(f"Error parsing expression: {e}")
            return None

    def find_intersections(self, x_vals):
        if self.fx is None or self.gx is None:
            return []  
        x_min = min(x_vals)
        x_max = max(x_vals)
        X= solve(self.fx - self.gx, self.x)
        X = [float(i) for i in X]
        intersections = []
        for x in X:
            y = float(self.gx.subs(self.x, x))
            if not (x < x_min or x > x_max):
                intersections.append((x, y))
        return intersections