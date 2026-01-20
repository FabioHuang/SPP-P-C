from PIL import Image
from PIL.Image import Image as PImage
from math import ceil
from pathlib import Path
from typing import Tuple

class ImageHandler():
    ''' Handles images with PIL Image '''
    def __init__(self):
        pass

    def crop_image(self, img: PImage, grid_resolution: float) -> PImage:
        ''' Crops and adds padding to images to fit in a grid with defined resolution '''
        # Ensure transparency layer
        if img.mode not in ('RGBA', 'LA'):
            img = img.convert('RGBA')

        bbox = img.getbbox()
        img = img.crop(bbox)
        
        # TODO Add padding...
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        new_w = ceil((w) / grid_resolution) * grid_resolution
        new_h = ceil((h) / grid_resolution) * grid_resolution
        
        grid_img = Image.new('RGBA', (new_w, new_h))
        print(img.size, grid_img.size)
        grid_img.paste(img, ((new_w - w) // 2, (new_h - h) // 2))
        
        grid_img.show()

        return grid_img

    def get_image(self, img_path: Path) -> PImage:
        return Image.open(img_path)

    def save_image(self, img: PImage, save_path: Path) -> bool:
        try:
            img_name = img.filename
            img.save(save_path / img_name)
            return True
    
        except FileNotFoundError:
            return False
    
    def get_size(self, img: PImage) -> Tuple[int, int]:
        return img.size

if __name__ == "__main__":
    car_path = Path("/home/ventilas/Pictures/car.png")
    resolution = 100
    handler = ImageHandler()
    img = handler.get_image(car_path)
    grid_img = handler.crop_image(img, resolution)
    grid_img.filename = "new_car.png"
    save_path = Path("/home/ventilas/Pictures/")
    handler.save_image(grid_img, save_path)
