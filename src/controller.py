from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMessageBox
import numpy as np

class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.ax = self.view.figure.gca()
        self.view.solve_btn.clicked.connect(self.solve)
        self.view.reset_btn.clicked.connect(self.reset)
        self.view.fx_plot_btn.clicked.connect(self.plot_fx)
        self.view.gx_plot_btn.clicked.connect(self.plot_gx)
        self.view.fit_btn.clicked.connect(self.fit_to_solution)

    def _validate_range(self):
        try:
            x_min = float(self.view.xmin_input.text())
            x_max = float(self.view.xmax_input.text())
            if x_min >= x_max:
                raise ValueError("X min must be less than X max.")
            return x_min, x_max
        except ValueError as e:
            QMessageBox.warning(self.view, "Input Error", f"Invalid range values: {e}")
            return None, None

    def _plot_functions(self, x_values):
        y_fx = self.model.evaluate(self.model.fx, x_values)
        y_gx = self.model.evaluate(self.model.gx, x_values)
        
        if np.isscalar(y_fx):
            y_fx = np.full_like(x_values, y_fx)
        if np.isscalar(y_gx):
            y_gx = np.full_like(x_values, y_gx)

        ax = self.view.figure.gca()
        ax.clear()
        if y_fx is not None:
            ax.plot(x_values, y_fx, label="f(x)", color="blue")
        if y_gx is not None:
            ax.plot(x_values, y_gx, label="g(x)", color="red")
        return ax
                
    @Slot()
    def plot_fx(self):
        fx_input = self.view.fx_input.text()
        if not fx_input.strip():
            QMessageBox.warning(self.view, "Input Error", "Please enter a function for f(x).")
            return
        self.model.set_fx(fx_input)
        self.plot()

    @Slot()
    def plot_gx(self):
        gx_input = self.view.gx_input.text()
        if not gx_input.strip():
            QMessageBox.warning(self.view, "Input Error", "Please enter a function for g(x).")
            return
        self.model.set_gx(gx_input)
        self.plot()

    @Slot()
    def plot(self):
        x_min, x_max = self._validate_range()
        x_values = np.linspace(x_min, x_max, 100)
        ax = self._plot_functions(x_values)
        ax.grid()
        ax.legend()
        self.view.canvas.draw()
        self.view.status_bar.showMessage("Plot updated.", 5000)

    @Slot()
    def solve(self):
        self.view.solutions_list.clear()
        
        if not self.view.fx_input.text().strip() or not self.view.gx_input.text().strip():
            QMessageBox.warning(self.view, "Input Error", "Please define both f(x) and g(x) before solving.")
            return

        self.model.set_fx(self.view.fx_input.text())
        self.model.set_gx(self.view.gx_input.text())

        x_min, x_max = self._validate_range()

        x_values = np.linspace(x_min, x_max, 1000)
        self.model.intersections = self.model.find_intersections(x_values)

        if not self.model.intersections:
            self.view.solutions_list.addItem("No solutions found.")
            QMessageBox.information(self.view, "No Intersections", "No intersection points were found.")
        else:
            for x, y in self.model.intersections:
                self.view.solutions_list.addItem(f"x = {x:.4f}, y = {y:.4f}")

        ax = self._plot_functions(x_values)
        ax.grid()
        self.model.annotate_solutions(self.ax)
        ax.legend()
        self.view.canvas.draw()
        self.view.status_bar.showMessage("Intersection points found and plotted.", 5000)

    @Slot()
    def fit_to_solution(self):
        if not self.model.intersections:
            QMessageBox.information(self.view, "No Solutions", 
                                  "No solutions available to fit to. Please solve the equations first.")
            return     
        self.model.zoom_to_intersections(self.ax)
        self.view.canvas.draw()
        self.view.status_bar.showMessage("Fitted view to solution points.", 5000)

    @Slot()
    def reset(self):
        self.view.fx_input.clear()
        self.view.gx_input.clear()
        self.view.xmin_input.setText("-10")
        self.view.xmax_input.setText("10")
        self.view.solutions_list.clear()    
        self.model.set_fx(None)
        self.model.set_gx(None)
        self.model.intersections = []     
        ax = self.view.figure.gca()
        ax.clear()
        ax.grid()        
        self.view.canvas.draw()  
        self.view.status_bar.showMessage("Reset complete.", 5000)