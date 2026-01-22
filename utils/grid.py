from image_handler import ImageHandler

from PIL import Image
from PIL.Image import Image as PImage
from uuid import uuid4
from pathlib import Path

from typing import List


class Grid():
    def __init__(self, width: float, resolution: float):
        self.W = width
        self.resolution = resolution

        self.handler = ImageHandler()

        self.items = {}

    def fit(self, solver) -> PImage:
        optimal_placement, H = solver.solve(self.items, self.W // self.resolution)
        
        optimal_grid = Image.new("RGBA", (self.W, H * self.resolution))
        
        for id, item in self.items.items():
            optimal_x, optimal_y = optimal_placement[id]
            optimal_grid.paste(item["image"], (optimal_x * self.resolution, optimal_y * resolution))

        return optimal_grid 

    def add(self, img: PImage | Path) -> None:
        if img.isinstance(Path):
            img = self.handler.get_image(img)
        
        img = self.handler.crop(img)

        # Sanity check
        assert img.size[0] % self.resolution == 0
        assert img.size[1] % self.resolution == 0
        assert img.mode in ("RGBA", "LA")

        id = str(uuid4())
        w, h = img.size

        self.items[id] = {'w': w // self.resolution, 'h': h // self.resolution, "image": img}

        return None

    def remove(self, item_id: int) -> None:
        del self.items[item_id]
        return None
    
    def list_items(self) -> List:
        return [item for item in self.items.keys()]

    def size(self) -> int:
        return len(self.items)

    def get_items(self) -> dict:
        return self.items
