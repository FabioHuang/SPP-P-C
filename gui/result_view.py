from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QScrollArea
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from PIL.ImageQt import ImageQt


class ResultDialog(QDialog):
    def __init__(self, pil_image, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Generated Image")
        self.resize(800, 600)

        self.pil_image = pil_image  # keep reference alive!

        image_qt = ImageQt(self.pil_image)
        self.pixmap = QPixmap.fromImage(image_qt)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setPixmap(self.pixmap)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.image_label)

        self.save_btn = QPushButton("Save image…")
        self.save_btn.clicked.connect(self.save_image)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        layout.addWidget(self.save_btn)

    def save_image(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save image",
            "result.png",
            "PNG Image (*.png);;JPEG Image (*.jpg)"
        )

        if not path:
            return

        try:
            self.pil_image.save(path)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Save failed",
                f"Could not save image:\n{e}"
            )

