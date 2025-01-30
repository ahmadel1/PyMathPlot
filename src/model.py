from sympy import symbols, sympify, lambdify, solve, exp, pi
import numpy as np
from PySide2.QtWidgets import QMessageBox

class FunctionModel:
    def __init__(self):
        self.x = symbols('x')
        self.locals = {"x": self.x, "X": self.x, "e": exp(1), "E": exp(1), "pi": pi}
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
            QMessageBox.warning(None, "Evaluation Error", f"Error evaluating function: {e}")
            print(f"Error evaluating function: {e}")
            return None

    def _parse_function(self, expression):
        expression = expression.strip()
        if not expression:
            QMessageBox.warning(None, "Input Error", "Expression cannot be empty.")
            return None
        try:
            expr = sympify(expression, convert_xor=True, evaluate=False, locals=self.locals)
            allowed_symbols = {self.x} 
            used_symbols = expr.free_symbols
            invalid_symbols = used_symbols - allowed_symbols
            
            if invalid_symbols:
                invalid_symbols_str = ', '.join(str(sym) for sym in invalid_symbols)
                QMessageBox.warning(None, "Input Error",
                                    f"Unknown symbol(s) used: {invalid_symbols_str}. Please use 'x' as the variable.")
                return None
            
            return expr
        except Exception as e:
            QMessageBox.warning(None, "Input Error", f"Invalid expression: {e}")
            print(f"Error parsing expression: {e}")
            return None

    def find_intersections(self, x_vals):
        if self.fx is None or self.gx is None:
            return []  
        x_min = min(x_vals)
        x_max = max(x_vals)
        try:
            X = solve(self.fx - self.gx, self.x)
        except Exception as e:
            QMessageBox.warning(None, "Solving Error", f"Unable to solve the equation f(x) = g(x): {e}")
            return []
        X = [float(i) for i in X]
        intersections = []
        for x in X:
            y = float(self.gx.subs(self.x, x))
            if not (x < x_min or x > x_max):
                intersections.append((x, y))
        return intersections