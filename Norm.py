import os
import time
from PIL import Image

def crop_image(input_image_path, output_image_path, left, top, right, bottom):      
    image = Image.open(input_image_path)
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save(output_image_path)
    # os.remove(input_image_path)
