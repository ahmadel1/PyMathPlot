import pytest
from PySide2.QtWidgets import QApplication
from src.view import MainWindow
from PySide2.QtCore import Qt

@pytest.fixture(scope="session")
def app():
    return QApplication.instance() or QApplication([])

@pytest.fixture
def gui(qtbot, app):
    view = MainWindow()
    qtbot.addWidget(view) 
    return view

def test_layout_structure(gui):
    assert gui.main_layout.count() > 0, "Main layout is empty"
    assert gui.left_panel.count() > 0, "Left panel layout is empty"
    assert gui.plot_layout.count() > 0, "Plot layout is empty"


def test_initial_label_text(gui):
    assert gui.fx_label.text() == "f(x) ="
    assert gui.gx_label.text() == "g(x) ="
    assert gui.xmin_label.text() == "X min:"
    assert gui.xmax_label.text() == "X max:"

def test_input_placeholders(gui):
    assert gui.fx_input.placeholderText() == "e.g., x^2 + x + 1"
    assert gui.gx_input.placeholderText() == "e.g., log10(x)"

def test_initial_button_labels(gui):
    assert gui.fx_plot_btn.text() == "Plot f(x)"
    assert gui.gx_plot_btn.text() == "Plot g(x)"
    assert gui.solve_btn.text() == "Solve"
    assert gui.reset_btn.text() == "Reset"
    assert gui.fit_btn.text() == "Fit to Points"

def test_initial_range_values(gui):
    assert gui.xmin_input.text() == "-10"
    assert gui.xmax_input.text() == "10"

def test_plot_canvas_exists(gui):
    assert gui.canvas is not None
    assert gui.toolbar is not None

def test_user_input(qtbot, gui):
    qtbot.keyClicks(gui.fx_input, "x^2 + 2*x + 1")
    assert gui.fx_input.text() == "x^2 + 2*x + 1"
    qtbot.keyClicks(gui.gx_input, "x + 1")
    assert gui.gx_input.text() == "x + 1"
    qtbot.mouseClick(gui.fx_plot_btn, Qt.LeftButton)

