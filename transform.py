import numpy as np
from PIL import Image, ImageDraw

from utils import get_dimensions

def crop_image(img: Image.Image, dimensions: str) -> Image.Image:
    return img


def square_image(img: Image.Image) -> Image.Image:
    w, h = img.size
    s = min([w, h])
    left = (w - s)/2
    top = (h - s)/2
    right = (w + s)/2
    bottom = (h + s)/2

    return img.crop((left, top, right, bottom)).resize((s, s), resample=Image.ANTIALIAS)


def round_image(img: Image.Image, radius: float = None) -> Image.Image:
    w, h = img.size
    resized = img.resize((h, w), Image.ANTIALIAS).convert("RGB")
    radius = radius if radius else max(h, w)

    # Round image
    npImage = np.array(resized)
    alpha = Image.new("L", resized.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.rounded_rectangle(((0, 0), (h, w)), radius, 255)

    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage, npAlpha))
    return Image.fromarray(npImage)


def fit_image(img: Image.Image, dimensions: str) -> Image.Image:
    w, h = get_dimensions(dimensions)
    oh, ow = img.size

    if w == 0 or h == 0:
        return img

    diff_w = ow - w
    diff_h = oh - h
    expansion_factor = 1

    if abs(diff_w) > abs(diff_h):
        expansion_factor = w / ow
    else:
        expansion_factor = h / ow

    w = round(ow * expansion_factor)
    h = round(oh * expansion_factor)
    print("Resizing", f"{ow}x{oh}", "to", f"{w}x{h}", "with a factor of", expansion_factor)

    img = img.resize((h, w), Image.ANTIALIAS)
    return img


def resize_image(img: Image.Image, dimensions: str) -> Image.Image:
    w, h = get_dimensions(dimensions)
    return img.resize((h, w), Image.ANTIALIAS)
