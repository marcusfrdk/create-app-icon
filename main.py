import argparse
import os
import time

import requests
import validators
from PIL import Image

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

  return vars(parser.parse_args())


class PathAction(argparse.Action):
  def __call__(self, parser, namespace, values, option_string=None):
    if validators.url(values):
      response = requests.get(values)
      content_type = response.headers.get("Content-Type")

      if not content_type.startswith("image/"):
        raise ValueError(f"Url '{values}' does not point to an image.")

      values = os.path.join(os.getcwd(), FETCH_FILE_NAME)
      with open(values, "wb+") as f:
        f.write(response.content)
    else:
      if not os.path.exists(values):
        raise FileNotFoundError(f"File '{values}' does not exist.")
    setattr(namespace, self.dest, values)


class CreateAppIcon():
  def __init__(self):
    self._args = get_args()
    self._name = os.path.splitext(os.path.basename(self._args["path"]))[0]
    self._output_path = os.path.join(os.getcwd(), f"output-{self._name}-{int(time.time())}")
    self._original = Image.open(self._args["path"]).convert("RGB")
    self._img = self._rescale(self._original, 1024)

    self._img.show()
    print(self._img.size)

  def _rescale(self, img: Image, max_size: int) -> Image:
    """ Rescale the image with the largest size equal to 'max_size'. """
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

  def resize(self, width: int, height: int) -> Image:
    """ Resize the image to the given width and height. """
    pass

  def rescale(self, max_size: int) -> Image:
    return self._rescale(self._img, max_size)

  def generate(self) -> None:
    """ Generate the selected icons. """
    pass


if __name__ == "__main__":
  CreateAppIcon()
