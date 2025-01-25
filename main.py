# main.py
import sys
from PySide2.QtWidgets import QApplication
from src.model import FunctionModel
from src.view import MainWindow
from src.controller import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = FunctionModel()
    view = MainWindow()
    controller = MainController(model, view)

    view.show()

    sys.exit(app.exec_())
