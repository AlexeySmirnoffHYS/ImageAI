import os
import time
from PIL import Image

def crop_image(input_image_path, output_image_path, left, top, right, bottom):
    image = Image.open(input_image_path)
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save(output_image_path)

input_path = "D:\\AI\\OpenAI\\Pictures\\Source\\"
output_path = "D:\\AI\\OpenAI\\Pictures\\Normolized\\"
left = 665
top = 95
right = 1044
bottom = 206

while True:
    image_files = [f for f in os.listdir(input_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    for image_file in image_files:
        print("Found new file:", image_file)
        input_image_path = os.path.join(input_path, image_file)
        output_image_path = os.path.join(output_path, image_file)
        
        crop_image(input_image_path, output_image_path, left, top, right, bottom)
        os.remove(input_image_path)
    
    time.sleep(5)
