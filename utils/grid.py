from PIL import Image
from PIL.Image import Image as PImage
from uuid import uuid64

from typing import List

class Grid():
    def __init__(self, width: float, resolution: float):
        self.W = width
        self.resolution = resolution

        self.items = {}

    def fit(self, solver) -> PImage:
        optimal_placement, H = solver.solve(self.items, self.W // self.resolution)
        
        optimal_grid = Image.new("RGBA", (self.W, H * self.resolution))
        
        for item in self.items:
            optimal_x, optimal_y = optimal_placement[item["id"]]
            optimal_grid.paste(item["image"], (optimal_x * self.resolution, optimal_y * resolution))

        return optimal_grid 

    def add(self, img: PImage) -> None:
        # Sanity check
        assert img.size[0] % resolution == 0
        assert img.size[1] % resolution == 0
        assert img.mode in ("RGBA", "LA")

        id = str(uuid64())
        w, h = img.size

        self.items[id] = {'w': w % resolution, 'h': h % resolution, "image": img}

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
