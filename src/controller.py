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
        y_fx, error = self.model.evaluate(self.model.fx, x_values)
        if error:
            QMessageBox.warning(self.view, "Evaluation Error", error)
            return None
            
        y_gx, error = self.model.evaluate(self.model.gx, x_values)
        if error:
            QMessageBox.warning(self.view, "Evaluation Error", error)
            return None
        
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
            
        success, error = self.model.set_fx(fx_input)
        if not success:
            QMessageBox.warning(self.view, "Input Error", error)
            return
            
        self.plot()

    @Slot()
    def plot_gx(self):
        gx_input = self.view.gx_input.text()
        if not gx_input.strip():
            QMessageBox.warning(self.view, "Input Error", "Please enter a function for g(x).")
            return
            
        success, error = self.model.set_gx(gx_input)
        if not success:
            QMessageBox.warning(self.view, "Input Error", error)
            return
            
        self.plot()

    @Slot()
    def plot(self):
        x_min, x_max = self._validate_range()
        if x_min is None or x_max is None:
            return
            
        x_values = np.linspace(x_min, x_max, 100)
        ax = self._plot_functions(x_values)
        if ax is None:
            return
            
        ax.grid()
        ax.legend()
        self.view.canvas.draw()
        self.view.status_bar.showMessage("Plot updated.", 5000)

    def _annotate_solutions(self, ax):
        for x, y in self.model.intersections:
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

    @Slot()
    def solve(self):
        self.view.solutions_list.clear()
        
        if not self.view.fx_input.text().strip() or not self.view.gx_input.text().strip():
            QMessageBox.warning(self.view, "Input Error", "Please define both f(x) and g(x) before solving.")
            return

        success, error = self.model.set_fx(self.view.fx_input.text())
        if not success:
            QMessageBox.warning(self.view, "Input Error", error)
            return
            
        success, error = self.model.set_gx(self.view.gx_input.text())
        if not success:
            QMessageBox.warning(self.view, "Input Error", error)
            return

        x_min, x_max = self._validate_range()
        if x_min is None or x_max is None:
            return

        x_values = np.linspace(x_min, x_max, 1000)
        intersections, error = self.model.find_intersections(x_values)
        
        if error:
            QMessageBox.warning(self.view, "Solving Error", error)
            return
            
        if not intersections:
            self.view.solutions_list.addItem("No solutions found.")
            QMessageBox.information(self.view, "No Intersections", "No intersection points were found.")
        else:
            for x, y in intersections:
                self.view.solutions_list.addItem(f"x = {x:.4f}, y = {y:.4f}")

        ax = self._plot_functions(x_values)
        if ax is None:
            return
            
        ax.grid()
        self._annotate_solutions(ax)
        ax.legend()
        self.view.canvas.draw()
        self.view.status_bar.showMessage("Intersection points found and plotted.", 5000)

    @Slot()
    def fit_to_solution(self):
        if not self.model.intersections:
            QMessageBox.information(self.view, "No Solutions", 
                                  "No solutions available to fit to. Please solve the equations first.")
            return
            
        bounds = self.model.get_intersection_view_bounds()
        if bounds:
            self.ax.set_xlim(bounds['x_min'], bounds['x_max'])
            self.ax.set_ylim(bounds['y_min'], bounds['y_max'])
            self._annotate_solutions(self.ax)
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