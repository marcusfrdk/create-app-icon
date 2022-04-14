import os
from PIL import Image

fp = os.path.abspath("images/landscape.jpg")
img = Image.open(fp)
name = img.filename
img = img.convert("RGB")

print(name)