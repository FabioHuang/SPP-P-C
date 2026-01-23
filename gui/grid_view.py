from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import QRect

from PIL.ImageQt import ImageQt
from pathlib import Path

class GridView(QWidget):
    SPACING = 10
    PADDING = 10

    def __init__(self, grid, parent=None):
        super().__init__(parent)

        self.grid = grid
        self.ui_rects = {}

        self.setAcceptDrops(True)
        self.setMinimumSize(400, 300)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            if url.isLocalFile():
                _ = self.grid.add(Path(url.toLocalFile()))
                self._recompute_layout()
                self.update()

    def _recompute_layout(self):
        self.ui_rects.clear()

        x = self.PADDING
        y = self.PADDING
        row_height = 0
        max_width = self.width() - self.PADDING

        for item_id, item in self.grid.get_items().items():
            w, h = item["image"].size

            if x + w > max_width:
                x = self.PADDING
                y += row_height + self.SPACING
                row_height = 0

            self.ui_rects[item_id] = QRect(x, y, w, h)

            x += w + self.SPACING
            row_height = max(row_height, h)

        self.setMinimumHeight(y + row_height + self.PADDING)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        for item_id, rect in self.ui_rects.items():
            item = self.grid.get_items().get(item_id)
            if not item:
                continue

            qimage = ImageQt(item["image"])
            pixmap = QPixmap.fromImage(qimage)
            painter.drawPixmap(rect, pixmap)

    def resizeEvent(self, event):
        self._recompute_layout()
        super().resizeEvent(event)

