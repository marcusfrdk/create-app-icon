import numpy as np
from PIL import Image, ImageDraw

def crop_image(img: Image.Image) -> Image.Image:
    w, h = img.size
    s = min([w, h])
    left = (w - s)/2
    top = (h - s)/2
    right = (w + s)/2
    bottom = (h + s)/2

    return img.crop((left, top, right, bottom)).resize((s, s), resample=Image.ANTIALIAS)


def round_image(img: Image.Image) -> Image.Image:
    w, h = img.size
    resized = img.resize((h, w), Image.ANTIALIAS).convert("RGB")

    # Round image
    npImage = np.array(resized)
    alpha = Image.new("L", resized.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage, npAlpha))
    return Image.fromarray(npImage)
