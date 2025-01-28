from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton,
    QLineEdit, QGroupBox, QSpacerItem, QSizePolicy, QMenuBar, QStatusBar, QListWidget
)
from PySide2.QtGui import QIntValidator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyMathPlotter")
        self.setStyleSheet("background-color: white;")
        self.resize(1000, 600)
        
        self.main_layout = QHBoxLayout(self)
        
        self.left_panel = QVBoxLayout()
        
        self.function_group = QGroupBox("Function Inputs")
        self.function_layout = QGridLayout()
        
        self.fx_label = QLabel("f(x) =")
        self.fx_input = QLineEdit()
        self.fx_input.setPlaceholderText('e.g., x^2 + x + 1')
        self.fx_plot_btn = QPushButton("Plot f(x)")
        self.function_layout.addWidget(self.fx_label, 0, 0)
        self.function_layout.addWidget(self.fx_input, 0, 1)
        self.function_layout.addWidget(self.fx_plot_btn, 0, 2)
        
        self.gx_label = QLabel("g(x) =")
        self.gx_input = QLineEdit()
        self.gx_input.setPlaceholderText('e.g., log10(x)')
        self.gx_plot_btn = QPushButton("Plot g(x)")
        self.function_layout.addWidget(self.gx_label, 1, 0)
        self.function_layout.addWidget(self.gx_input, 1, 1)
        self.function_layout.addWidget(self.gx_plot_btn, 1, 2)
        
        self.function_group.setLayout(self.function_layout)
        self.left_panel.addWidget(self.function_group)
        
        self.range_group = QGroupBox("Plot Range")
        self.range_layout = QGridLayout()
        
        self.xmin_label = QLabel("X min:")
        self.xmin_input = QLineEdit("-10")
        self.xmin_input.setValidator(QIntValidator())
        self.xmax_label = QLabel("X max:")
        self.xmax_input = QLineEdit("10")
        self.xmax_input.setValidator(QIntValidator())
        
        self.range_layout.addWidget(self.xmin_label, 0, 0)
        self.range_layout.addWidget(self.xmin_input, 0, 1)
        self.range_layout.addWidget(self.xmax_label, 1, 0)
        self.range_layout.addWidget(self.xmax_input, 1, 1)
        
        self.range_group.setLayout(self.range_layout)
        self.left_panel.addWidget(self.range_group)
        
        self.actions_group = QGroupBox("Actions")
        self.actions_layout = QHBoxLayout()
        self.solve_btn = QPushButton("Solve")
        self.reset_btn = QPushButton("Reset")
        self.actions_layout.addWidget(self.solve_btn)
        self.actions_layout.addWidget(self.reset_btn)
        self.actions_group.setLayout(self.actions_layout)
        self.left_panel.addWidget(self.actions_group)
        
        self.solutions_group = QGroupBox("Solutions")
        self.solutions_layout = QVBoxLayout()
        self.solutions_list = QListWidget()
        self.solutions_layout.addWidget(self.solutions_list)
        self.solutions_group.setLayout(self.solutions_layout)
        self.left_panel.addWidget(self.solutions_group)
        
        self.left_panel.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.status_bar = QStatusBar()
        self.left_panel.addWidget(self.status_bar)
        
        self.apply_styles()
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumWidth(600)
        self.canvas.setMinimumHeight(500)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.plot_layout = QVBoxLayout()
        self.plot_layout.addWidget(self.canvas)
        self.plot_layout.addWidget(self.toolbar)
        
        self.main_layout.addLayout(self.left_panel, 1)
        self.main_layout.addLayout(self.plot_layout, 3)
        
        self.setLayout(self.main_layout)
        
    def apply_styles(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                font-size: 14px;
                height: 25px;
            }
            QPushButton {
                font-size: 14px;
                width: 80px;
                height: 30px;
            }
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
            }
            QStatusBar {
                font-size: 12px;
            }
            QListWidget {
                font-size: 14px;
            }
        """)