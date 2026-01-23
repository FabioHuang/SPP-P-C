from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QScrollArea, QApplication
from utils.grid import Grid
from gui.grid_view import GridView
from gui.result_view import ResultDialog
from solver.model import SCIPSolver

from os import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grid Optimizer")
        self.resize(900, 600)

        self.grid = Grid(width=1000, resolution=80)
        self.solver = SCIPSolver()

        self.grid_view = GridView(self.grid)

        self.generate_btn = QPushButton("Generate optimal layout")
        self.generate_btn.clicked.connect(self.generate)

        container = QWidget()
        layout = QVBoxLayout(container)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.grid_view)

        layout.addWidget(scroll)
        layout.addWidget(self.generate_btn)

        self.setCentralWidget(container)

    def generate(self):
        if self.grid.size() == 0:
            return
        
        result_image = self.grid.fit(self.solver)
        dialog = ResultDialog(result_image, self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

