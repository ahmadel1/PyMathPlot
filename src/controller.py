from PySide2.QtCore import Slot

class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.solve_btn.clicked.connect(self.solve)
        self.view.reset_btn.clicked.connect(self.reset)

    @Slot()
    def solve(self):
        fx_input = self.view.fx_input.text()
        gx_input = self.view.gx_input.text()

        self.model.set_fx(fx_input)
        self.model.set_gx(gx_input)

        x_values = list(range(-10, 11))  
        y_fx = self.model.evaluate(self.model.fx, x_values)
        y_gx = self.model.evaluate(self.model.gx, x_values)

        ax = self.view.figure.gca()
        ax.clear()  

        if y_fx:
            ax.plot(x_values, y_fx, label="f(x)", color="blue")
        if y_gx:
            ax.plot(x_values, y_gx, label="g(x)", color="red")

        ax.legend()
        self.view.canvas.draw()

    @Slot()
    def reset(self):
        self.view.fx_input.clear()
        self.view.gx_input.clear()
        ax = self.view.figure.gca()
        ax.clear() 
        self.view.canvas.draw()
