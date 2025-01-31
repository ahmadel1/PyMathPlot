import pytest
from unittest.mock import Mock, patch
import numpy as np
from src.controller import MainController
from PySide2.QtWidgets import QMessageBox

class TestMainController:
    @pytest.fixture
    def mock_controller(self):
        model = Mock()
        view = Mock()
        controller = MainController(model, view)
        return controller, model, view

    def test_validate_range_valid(self, mock_controller):
        controller, _, view = mock_controller
        view.xmin_input.text.return_value = "0"
        view.xmax_input.text.return_value = "10"
        
        x_min, x_max = controller._validate_range()
        
        assert x_min == 0
        assert x_max == 10

    def test_validate_range_invalid(self, mock_controller):
        controller, _, view = mock_controller
        view.xmin_input.text.return_value = "10"
        view.xmax_input.text.return_value = "0"
        
        with patch('PySide2.QtWidgets.QMessageBox.warning') as mock_warning:
            x_min, x_max = controller._validate_range()
            
            mock_warning.assert_called_once()
            assert x_min is None
            assert x_max is None

    def test_solve_no_functions(self, mock_controller):
        controller, _, view = mock_controller
        view.fx_input.text.return_value = ""
        view.gx_input.text.return_value = ""
        
        with patch('PySide2.QtWidgets.QMessageBox.warning') as mock_warning:
            controller.solve()
            mock_warning.assert_called_once()

    def test_solve_with_intersections(self, mock_controller):
        controller, model, view = mock_controller
        model.set_fx.return_value = (True, None)
        model.set_gx.return_value = (True, None)
        model.intersections = [(1.5, 2.25), (3.0, 4.5)]
        
        x_values = np.linspace(-5, 5, 1000)
        model.evaluate = Mock(side_effect=[
            (np.zeros_like(x_values), None),  # y_fx
            (np.zeros_like(x_values), None)   # y_gx
        ])
        model.find_intersections_symbolic.return_value = (model.intersections, None)
        
        view.fx_input.text.return_value = "x**2"
        view.gx_input.text.return_value = "x"
        view.xmin_input.text.return_value = "-5"
        view.xmax_input.text.return_value = "5"
        view.accuracy_combo.currentText.return_value = "High"
        view.method_combo.currentText.return_value = "Symbolic"
        view.figure.gca.return_value = Mock()
        view.canvas.draw = Mock()
        
        controller.solve()
        view.solutions_list.addItem.assert_any_call("x = 1.5000, y = 2.2500")
        view.solutions_list.addItem.assert_any_call("x = 3.0000, y = 4.5000")

    def test_reset(self, mock_controller):
        controller, model, view = mock_controller
        controller.reset()
        
        view.fx_input.clear.assert_called_once()
        view.gx_input.clear.assert_called_once()
        view.solutions_list.clear.assert_called_once()
        
        view.xmin_input.setText.assert_called_with("-10")
        view.xmax_input.setText.assert_called_with("10")

    def test_plot_functions(self, mock_controller):
        controller, model, view = mock_controller
        
        x_values = np.linspace(0, 10, 100)
        model.evaluate.side_effect = [
            (np.sin(x_values), None), 
            (np.cos(x_values), None)  
        ]
        
        ax = controller._plot_functions(x_values)
        
        assert ax is not None