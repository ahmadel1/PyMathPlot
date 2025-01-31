from sympy import symbols, sympify, lambdify, solve, exp, pi
import numpy as np

class FunctionModel:
    def __init__(self):
        self.x = symbols('x')
        self.locals = {"x": self.x, "X": self.x, "e": exp(1), "E": exp(1), "pi": pi}
        self.fx = None       
        self.gx = None 
        self.intersections = []
  
    def set_fx(self, expression):
        if expression is None:
            self.fx = None
            return True, None
        
        if not expression.strip():
            return False, "Expression cannot be empty."
            
        try:
            expr = self._parse_expression(expression)
            if expr is None:
                return False, "Invalid expression format."
            self.fx = expr
            return True, None
        except Exception as e:
            return False, f"Error parsing expression: {str(e)}"

    def set_gx(self, expression):
        if expression is None:
            self.gx = None
            return True, None
            
        if not expression.strip():
            return False, "Expression cannot be empty."
            
        try:
            expr = self._parse_expression(expression)
            if expr is None:
                return False, "Invalid expression format."
            self.gx = expr
            return True, None
        except Exception as e:
            return False, f"Error parsing expression: {str(e)}"

    def evaluate(self, func, x_values):
        if func is None:
            return None, None
        try:
            x_vals = np.array(x_values)
            func_lambda = lambdify(self.x, func, "numpy")
            return func_lambda(x_vals), None
        except Exception as e:
            return None, f"Error evaluating function: {str(e)}"

    def _parse_expression(self, expression):
        expr = sympify(expression, convert_xor=True, evaluate=False, locals=self.locals)
        allowed_symbols = {self.x} 
        used_symbols = expr.free_symbols
        invalid_symbols = used_symbols - allowed_symbols
        
        if invalid_symbols:
            invalid_symbols_str = ', '.join(str(sym) for sym in invalid_symbols)
            raise ValueError(f"Unknown symbol(s) used: {invalid_symbols_str}. Please use 'x' as the variable.")
        
        return expr

    def find_intersections(self, x_vals):
        self.intersections = []
        if self.fx is None or self.gx is None:
            return [], None
            
        x_min = min(x_vals)
        x_max = max(x_vals)
        try:
            X = solve(self.fx - self.gx, self.x)
            X = [sol for sol in X if sol.is_real]
            X = [float(i) for i in X]
            
            for x in X:
                if x_min <= x <= x_max:
                    y = float(self.gx.subs(self.x, x))
                    self.intersections.append((x, y))
            return self.intersections, None
        except Exception as e:
            return [], f"Unable to solve the equation f(x) = g(x): {str(e)}"

    def get_intersection_view_bounds(self):
        if not self.intersections:
            return None
            
        x_values = [x for x, _ in self.intersections]
        y_values = [y for _, y in self.intersections]
        
        if len(self.intersections) == 1:
            x_mid = x_values[0]
            y_mid = y_values[0]
            return {
                'x_min': x_mid - 2,
                'x_max': x_mid + 2,
                'y_min': y_mid - 2,
                'y_max': y_mid + 2
            }
        else:
            x_range = max(x_values) - min(x_values)
            y_range = max(y_values) - min(y_values)
            x_padding = 0.6 * x_range
            y_padding = 0.6 * y_range
            return {
                'x_min': min(x_values) - x_padding,
                'x_max': max(x_values) + x_padding,
                'y_min': min(y_values) - y_padding,
                'y_max': max(y_values) + y_padding
            }