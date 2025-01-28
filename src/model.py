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
            # Replace '^' with '**' for exponentiation
            expression = expression.replace('^', '**')
            return sympify(expression, evaluate=False)
        except Exception as e:
            print(f"Error parsing expression: {e}")
            return None

    def find_intersections(self, x_values):
        if self.fx is None or self.gx is None:
            return []

        x_min = min(x_values)
        x_max = max(x_values)

        f_func = lambdify(self.x, self.fx, 'numpy')
        g_func = lambdify(self.x, self.gx, 'numpy')
        h_func = lambda x: f_func(x) - g_func(x)

        x_vals = np.linspace(x_min, x_max, 1000)
        h_vals = h_func(x_vals)

        sign_changes = np.where(np.diff(np.sign(h_vals)))[0]

        intersections = []
        for idx in sign_changes:
            x0 = x_vals[idx]
            x1 = x_vals[idx + 1]
            try:
                root = fsolve(h_func, (x0 + x1) / 2)
                x_root = root[0]
                if x_min <= x_root <= x_max:
                    y_root = f_func(x_root)
                    intersections.append((x_root, y_root))
            except Exception as e:
                print(f"Error finding root between {x0} and {x1}: {e}")

        return intersections