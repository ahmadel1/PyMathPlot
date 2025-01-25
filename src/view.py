from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFrame
)
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Playground")
        self.resize(800, 600)
        self.main_layout = QHBoxLayout()  
        self.left_layout = QVBoxLayout()

        self.fx_layout = QVBoxLayout()
        self.fx_input = QLineEdit()
        self.fx_label = QLabel("f(x)")
        self.fx_preview = QLabel("Enter f(x) in LaTeX here")
        self.fx_layout.addWidget(self.fx_label)
        self.fx_layout.addWidget(self.fx_input)

        self.gx_layout = QVBoxLayout()
        self.gx_input = QLineEdit()
        self.gx_label = QLabel("g(x)")
        self.gx_layout.addWidget(self.gx_label)
        self.gx_layout.addWidget(self.gx_input)

        self.button_layout = QHBoxLayout()
        self.solve_btn = QPushButton("Solve")
        self.reset_btn = QPushButton("Reset")
        button_width = 150
        self.solve_btn.setFixedWidth(button_width)
        self.reset_btn.setFixedWidth(button_width)
        self.button_layout.addWidget(self.solve_btn)
        self.button_layout.addWidget(self.reset_btn)

        self.left_layout.addLayout(self.fx_layout)
        self.left_layout.addLayout(self.gx_layout)
        self.left_layout.addLayout(self.button_layout)
        self.left_layout.addStretch()

        self.figure = plt.figure()
        ax = self.figure.subplots()
        self.x = range(10)
        self.y = range(10)
        ax.plot(self.x, self.y)


        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumWidth(500) 
        self.canvas.setMinimumHeight(500)
    

        self.main_layout.addLayout(self.left_layout, stretch=1)  
        self.main_layout.addWidget(self.canvas, stretch=5)  
        self.setLayout(self.main_layout)


