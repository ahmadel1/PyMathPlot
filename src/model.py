from sympy import symbols, sympify, lambdify, solve, exp, pi
import numpy as np
from scipy.optimize import brentq

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

    def find_intersections_symbolic(self, x_vals):
        self.intersections = []
        if self.fx is None or self.gx is None:
            return [], None
        if self.fx == self.gx:
            return [], "There are Infinite number of solutions found"
        
        x_vals = np.array(x_vals, dtype=np.float64)
        x_min, x_max = np.min(x_vals), np.max(x_vals)
        
        try:
            symbolic_roots = solve(self.fx - self.gx, self.x)
            symbolic_roots = [sol for sol in symbolic_roots if sol.is_real]
            
            for root in symbolic_roots:
                x_root_float = float(root.evalf())
                
                if x_min - 1e-9 <= x_root_float <= x_max + 1e-9:
                    y_root = self.evaluate(self.fx, [x_root_float])        
                    if y_root is not None and len(y_root) > 0 and not np.isnan(y_root[0][0]):
                        self.intersections.append((x_root_float, y_root[0][0]))     
            return self.intersections, None
        
        except Exception as e:
            return [], f"Unable to solve the equation f(x) = g(x): {str(e)}"
    
    def find_intersections_numerical(self, x_vals, tol=1e-6):
        self.intersections = []
        if self.fx is None or self.gx is None:
            return [], None
        if self.fx == self.gx:
            return [], "There are infinite solutions"

        x_vals = np.array(x_vals, dtype=np.float64)
        x_min, x_max = x_vals.min(), x_vals.max()

        def diff_func(x):
            fx = self.evaluate(self.fx, x)
            gx = self.evaluate(self.gx, x)
            fx = fx[0] if isinstance(fx, (list, tuple, np.ndarray)) else fx
            gx = gx[0] if isinstance(gx, (list, tuple, np.ndarray)) else gx
            return fx - gx

        diff_vals = np.array([diff_func(x) for x in x_vals])
        sign_changes = np.where(np.diff(np.sign(diff_vals)))[0]

        for i in sign_changes:
            x_left, x_right = x_vals[i], x_vals[i + 1]
            try:
                root = brentq(diff_func, x_left, x_right, xtol=tol)
                if x_min - 1e-9 <= root <= x_max + 1e-9:
                    y_root = self.evaluate(self.fx, root)
                    y_root = y_root[0] if isinstance(y_root, (list, tuple, np.ndarray)) else y_root
                    if y_root is not None and not np.isnan(y_root):
                        self.intersections.append((root, y_root))
            except ValueError:
                continue

        return self.intersections, None


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