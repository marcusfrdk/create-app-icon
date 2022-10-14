import argparse
import os
import time

import numpy as np
import requests
import validators
from PIL import Image, ImageDraw

FETCH_FILE_NAME = ".create-app-icon.jpg"


def get_args() -> dict:
  parser = argparse.ArgumentParser(description="Generate all icons required for an application.")

  # Required
  parser.add_argument("path", help="path to an image file", type=str, action=PathAction)

  # Devices
  parser.add_argument("--ios", help="generate icons for ios.", action="store_true")
  parser.add_argument("--ipad", help="generate icons for the iPad.", action="store_true")
  parser.add_argument("--apple-watch", help="generate icons for the Apple Watch.", action="store_true")
  parser.add_argument("--android", help="generate icons for Android.", action="store_true")
  parser.add_argument("--web", help="generate icons for websites.", action="store_true")

  # Config
  parser.add_argument("-r", "--radius", help="sets the border radius of the favicon.", type=int, default=0)
  parser.add_argument("-v", "--verbose", help="output more to terminal", action="store_true")
  parser.add_argument(
    "-a",
    "--align",
    help="aligns the image vertically.",
    type=str,
    choices=["top", "right", "bottom", "left"],
    action=AlignAction,
    nargs="+"
  )

  return vars(parser.parse_args())


class PathAction(argparse.Action):
  def __call__(self, parser, namespace, values, option_string=None):
    if validators.url(values):
      response = requests.get(values)
      content_type = response.headers.get("Content-Type")

      if content_type.lower() not in ["image/jpeg", "image/jpg", "image/png"]:
        raise ValueError(f"Url '{values}' does not point to an image.")

      values = os.path.join(os.getcwd(), FETCH_FILE_NAME)
      with open(values, "wb+") as f:
        f.write(response.content)
    else:
      if not os.path.exists(values):
        raise FileNotFoundError(f"File '{values}' does not exist.")
    setattr(namespace, self.dest, values)


class AlignAction(argparse.Action):
  def __call__(self, parser, namespace, values, option_string=None):
    if len(values) > 2:
      raise ValueError("You can only specify 2 alignments.")
    if "top" in values and "bottom" in values:
      raise ValueError("Top- and bottom alignments are exclusive.")
    if "left" in values and "right" in values:
      raise ValueError("Left- and right alignments are exclusive.")
    setattr(namespace, self.dest, values)


class CreateAppIcon():
  def __init__(self):
    self._args = get_args()
    self._name = os.path.splitext(os.path.basename(self._args["path"]))[0]
    self._output_path = os.path.join(os.getcwd(), f"output-{self._name}-{int(time.time())}")
    self._org = Image.open(self._args["path"]).convert("RGB")

    if self._args["align"]:
      self._img = self.crop(1024, 1024, img=self.rescale(2048, img=self._org))
    else:
      self._img = self.rescale(1024, img=self._org)

  def crop(
      self,
      width: int = None,
      height: int = None,
      img: Image = None
  ) -> Image:
    """ 
      Returns a cropped image, if no width and height are provided, 
      it will square the image with the smallest of the original 
      images dimensions. 
    """
    img = img if img else self._img
    w, h = img.size

    # Set minimum width and height
    if width and height:
      mx, my = width, height
    else:
      mx = my = min(img.size)

    left = (w - mx) / 2
    top = (h - my) / 2
    right = (w + mx) / 2
    bottom = (h + my) / 2

    # Alignment
    align = self._args["align"] or []
    if "top" in align:
      top, bottom = 0, my
    elif "bottom" in align:
      top, bottom = h - my, h
    if "left" in align:
      left, right = 0, mx
    elif "right" in align:
      left, right = w - mx, w

    return img.crop((left, top, right, bottom)).resize((mx, my), Image.ANTIALIAS)

  def rescale(self, max_size: int, img: Image = None) -> Image:
    """ Rescale the image with the largest size equal to 'max_size'. """
    img = img if img else self._img
    w, h = img.size

    if max_size > min(w, h):
      # Upscale image
      ratio = max(w, h) / min(w, h)
      width = max_size if w < h else round(max_size * ratio)
      height = round(max_size * ratio) if w < h else max_size
      return img.resize((width, height), Image.ANTIALIAS)

    # Downscale image
    ratio = min(w, h) / max(w, h)

    if w > h:
      # Landscape
      width = max_size
      height = round(max_size * ratio)
    else:
      # Portrait
      width = round(max_size * ratio)
      height = max_size

    return img.resize((width, height), Image.ANTIALIAS)

  def resize(self, width: int, height: int = None, img: Image = None) -> Image:
    """ Resize the image to the specified width and height. """
    img = img if img else self._img
    height = height if height else width
    return img.resize((width, height), Image.ANTIALIAS)

  def round(self, radius: int = None, img: Image = None) -> Image:
    img = img if img else self._img
    w, h = img.size
    radius = radius if radius else max(img.size)
    np_img = np.array(img)
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.rounded_rectangle(((0, 0), (h, w)), radius, 255)
    np_alpha = np.array(alpha)
    np_img = np.dstack((np_img, np_alpha))
    return Image.fromarray(np_img)

  def favicon(self) -> Image:
    """ Returns an image with the size of a favicon, you still have to save it as a favicon. """
    return self._round(self._crop(self._rescale(self._img, 512), (512, 512)))

  @property
  def img(self) -> Image:
    return self._img

  @property
  def org(self) -> Image:
    return self._org


if __name__ == "__main__":
  icon = CreateAppIcon()
  # icon._original.show()
  # icon.favicon().save("./favicon.ico", format="ICO", optimize=True, icc_profile=None)
  # icon._img.show()
  # icon.crop(512, 512).show()

  icon.crop().show()
