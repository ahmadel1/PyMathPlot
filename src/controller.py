from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMessageBox, QFileDialog

import numpy as np
import math
import matplotlib.ticker as ticker

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
        self.view.save_action.triggered.connect(self.save_solution)

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
    

    def _format_si(self, value, _=1):
        si_prefixes = [
            (-18, 'a'), (-15, 'f'), (-12, 'p'), (-9, 'n'),
            (-6, 'µ'), (-3, 'm'), (0, ''), (3, 'k'),
            (6, 'M'), (9, 'G'), (12, 'T'), (15, 'P'),
            (18, 'E'), (21, 'Z'), (24, 'Y')
        ]
        if value == 0:
            return "0 "  # Special case for zero

        abs_value = abs(value)
        exponent = math.floor(math.log10(abs_value))
        si_exponent = min(max((exponent // 3) * 3, -18), 24)
        scaled_value = round(value / 10**si_exponent, 1)

        # Use list indexing for lookup
        prefix = si_prefixes[(si_exponent + 18) // 3][1]

        return f"{scaled_value:.1f}{prefix}"
                
    def _get_plot_points(self):
        """Calculate number of points based on range and accuracy setting"""
        try:
            x_min = float(self.view.xmin_input.text())
            x_max = float(self.view.xmax_input.text())
            range_size = abs(x_max - x_min)

            accuracy = self.view.accuracy_combo.currentText()

            # Base number of points for different accuracies
            points_map = {
                "Low": 100,
                "Medium": 500,
                "High": 1000
            }

            # Adjust points based on range size
            base_points = points_map[accuracy]
            range_factor = max(1, range_size / 20)  # Normalize to a standard range of 20
            return int(base_points * range_factor)

        except ValueError:
            return 1000  # fallback
            
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
            
        num_points = self._get_plot_points()
        x_values = np.linspace(x_min, x_max, num_points)
        ax = self._plot_functions(x_values)
        if ax is None:
            return
            
        ax.grid()
        ax.legend()
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self._format_si))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(self._format_si))
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

        num_points = self._get_plot_points()
        x_values = np.linspace(x_min, x_max, num_points)
        intersections, error = self.model.find_intersections_symbolic(x_values)
        
        if error == "There are Infinite number of solutions found":
            self.view.solutions_list.addItem("Infinite number of solutions found")
            QMessageBox.information(self.view, "Infinite Solutions", "There are Infinite number of solutions found.")
        elif error:
            QMessageBox.warning(self.view, "Solving Error", error)
            return
        elif not intersections:
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
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self._format_si))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(self._format_si))
        self.view.canvas.draw()
        if not len(intersections) == 0:
            self.view.status_bar.showMessage("Intersection points found and plotted.", 5000)
        elif error == "There are Infinite number of solutions found":
            self.view.status_bar.showMessage("Infinite number of solutions found", 5000)
        else: 
            self.view.status_bar.showMessage("no solutions found", 5000)


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

    

    @Slot()
    def save_solution(self):
        # Open file dialog to choose save location and filename
        file_path, _ = QFileDialog.getSaveFileName(
            self.view, 
            "Save Plot", 
            "", 
            "PNG Files (*.png);;All Files (*)"
        )
        
        # Check if a file path was selected
        if file_path:
            try:
                # Save the figure to the selected file path
                self.ax.figure.savefig(file_path, bbox_inches='tight')
                self.view.status_bar.showMessage(f"Plot saved to {file_path}", 5000)
            except Exception as e:
                QMessageBox.warning(
                    self.view, 
                    "Save Error", 
                    f"Could not save the plot: {str(e)}"
                )