from sympy import symbols, sympify, lambdify, solve, exp, pi
import numpy as np
from PySide2.QtWidgets import QMessageBox

class FunctionModel:
    def __init__(self):
        self.x = symbols('x')
        self.locals = {"x": self.x, "X": self.x, "e": exp(1), "E": exp(1), "pi": pi}
        self.fx = None       
        self.gx = None 
        self.intersections = []
  

    def set_fx(self, expression):
        self.fx = self.parse_function(expression)

    def set_gx(self, expression):
        self.gx = self.parse_function(expression)

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

    def parse_function(self, expression):
        if expression is None:
            return None
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
            X = [sol for sol in X if sol.is_real]
        except Exception as e:
            QMessageBox.warning(None, "Solving Error", f"Unable to solve the equation f(x) = g(x): {e}")
            return []
        print(X)
        X = [float(i) for i in X]
        for x in X:
            y = float(self.gx.subs(self.x, x))
            if not (x < x_min or x > x_max):
                self.intersections.append((x, y))
        return self.intersections
    
    def annotate_solutions(self, ax):
        for x, y in self.intersections:
                ax.plot(x, y, 'ko')
                ax.annotate(
                    f"({x:.2f}, {y:.2f})",
                    xy=(x, y),
                    textcoords="offset points",
                    xytext=(10, 10),
                    fontsize=10,
                    fontweight='bold',
                    bbox=dict(facecolor="white", alpha=0.7, edgecolor="black", boxstyle="round,pad=0.3"),
                )

    def zoom_to_intersections(self, ax):
        if not self.intersections:
            return
            
        x_values = [x for x, _ in self.intersections]
        y_values = [y for _, y in self.intersections]
        
        if len(self.intersections) == 1:
            x_range = 2
            y_range = 2
            x_mid = x_values[0]
            y_mid = y_values[0]
            ax.set_xlim(x_mid - x_range, x_mid + x_range)
            ax.set_ylim(y_mid - y_range, y_mid + y_range)
        else:
            x_range = max(x_values) - min(x_values)
            y_range = max(y_values) - min(y_values)
            x_padding = 0.6 * x_range
            y_padding = 0.6 * y_range
            ax.set_xlim(min(x_values) - x_padding, max(x_values) + x_padding)
            ax.set_ylim(min(y_values) - y_padding, max(y_values) + y_padding)
        
        self.annotate_solutions(ax)
    
 