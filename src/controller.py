from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMessageBox
import numpy as np

class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.solve_btn.clicked.connect(self.solve)
        self.view.reset_btn.clicked.connect(self.reset)
        self.view.fx_plot_btn.clicked.connect(self.plot_fx)
        self.view.gx_plot_btn.clicked.connect(self.plot_gx)

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
        try:
            x_min = float(self.view.xmin_input.text())
            x_max = float(self.view.xmax_input.text())
            if x_min >= x_max:
                raise ValueError("X min must be less than X max.")
        except ValueError as e:
            QMessageBox.warning(self.view, "Input Error", f"Invalid range values: {e}")
            return

        x_values = np.linspace(x_min, x_max, 1000)
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
        
        ax.grid()
        ax.legend()
        self.view.canvas.draw()
        self.view.status_bar.showMessage("Plot updated.", 5000)  # Message displayed for 5 seconds

    @Slot()
    def solve(self):
        self.view.solutions_list.clear()
        
        fx_input = self.view.fx_input.text()
        gx_input = self.view.gx_input.text()
        self.model.set_fx(fx_input)
        self.model.set_gx(gx_input)

        if self.model.fx is None or self.model.gx is None:
            QMessageBox.warning(self.view, "Input Error", "Please define both f(x) and g(x) before solving.")
            return

        try:
            x_min = float(self.view.xmin_input.text())
            x_max = float(self.view.xmax_input.text())
            if x_min >= x_max:
                raise ValueError("X min must be less than X max.")
        except ValueError as e:
            QMessageBox.warning(self.view, "Input Error", f"Invalid range values: {e}")
            return

        x_values = np.linspace(x_min, x_max, 1000)
        intersections = self.model.find_intersections(x_values)

        if not intersections:
            self.view.solutions_list.addItem("No solutions found.")
            QMessageBox.information(self.view, "No Intersections", "No intersection points were found.")
        else:
            for x, y in intersections:
                solution_text = f"x = {x:.4f}, y = {y:.4f}"
                self.view.solutions_list.addItem(solution_text)
        
        ax = self.view.figure.gca()

        ax.clear()
        y_fx = self.model.evaluate(self.model.fx, x_values)
        y_gx = self.model.evaluate(self.model.gx, x_values)
        
        if np.isscalar(y_fx):
            y_fx = np.full_like(x_values, y_fx)

        if np.isscalar(y_gx):
            y_gx = np.full_like(x_values, y_gx)
            
        if y_fx is not None:
            ax.plot(x_values, y_fx, label="f(x)", color="blue")
        if y_gx is not None:
            ax.plot(x_values, y_gx, label="g(x)", color="red")

        x_values_for_zoom = [x for x, _ in intersections]
        y_values_for_zoom = [y for _, y in intersections]
        x_range = max(x_values_for_zoom) - min(x_values_for_zoom)
        y_range = max(y_values_for_zoom) - min(y_values_for_zoom)

        x_padding = 0.6 * x_range
        y_padding = 0.6 * y_range
        x_min_zoom = min(x_values_for_zoom) - x_padding
        x_max_zoom = max(x_values_for_zoom) + x_padding
        y_min_zoom = min(y_values_for_zoom) - y_padding
        y_max_zoom = max(y_values_for_zoom) + y_padding

        ax.set_xlim(x_min_zoom, x_max_zoom)
        ax.set_ylim(y_min_zoom, y_max_zoom)
      
        for x, y in intersections:
            ax.plot(x, y, 'ko')  
            ax.annotate(f"({x:.2f}, {y:.2f})", xy=(x, y), textcoords="offset points", xytext=(10, 10), ha='center', va='center')

        ax.grid()
        ax.legend()
        self.view.canvas.draw()
        self.view.status_bar.showMessage("Intersection points found and plotted.", 5000)

    @Slot()
    def reset(self):
        self.view.fx_input.clear()
        self.view.gx_input.clear()
        self.model.set_fx(None)
        self.model.set_gx(None)
        self.view.xmin_input.setText("-10")
        self.view.xmax_input.setText("10")
        self.view.solutions_list.clear()
        ax = self.view.figure.gca()
        ax.clear()
        ax.grid()
        self.view.canvas.draw()
        self.view.status_bar.showMessage("Reset complete.", 5000)