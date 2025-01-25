from sympy import symbols, sympify, lambdify

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
            func_lambda = lambdify(self.x, func, "numpy")
            return [func_lambda(x) for x in x_values]
        except Exception as e:
            print(f"Error evaluating function: {e}")
            return None

    def _parse_function(self, expression):
        try:
            return sympify(expression)
        except Exception as e:
            print(f"Error parsing expression: {e}")
            return None
