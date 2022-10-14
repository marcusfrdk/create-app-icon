import argparse
import json
import os
import time
from enum import Enum

import numpy as np
import requests
import validators
from PIL import Image, ImageDraw

FETCH_FILE_NAME = ".create-app-icon.jpg"
PRESETS = ["ios", "ipad", "apple_watch", "android", "web"]


class Preset(Enum):
  IOS = "ios"
  IPAD = "ipad"
  APPLE_WATCH = "apple_watch"
  ANDROID = "android"
  WEB = "web"


def read_preset(name: str) -> list:
  with open(os.path.join(os.path.dirname(__file__), "presets.json"), "r", encoding="utf-8") as f:
    return json.load(f)[name]


def get_args() -> dict:
  """ Read and returns the command line arguments. """
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
    self._name = os.path.splitext(os.path.basename(self._args["path"]))[
        0] if FETCH_FILE_NAME not in self._args["path"] else "fetch"
    self._output_path = os.path.join(os.getcwd(), f"output-{self._name}-{int(time.time())}")
    self._org = Image.open(self._args["path"]).convert("RGB")
    self._presets = json.load(open(os.path.join(os.path.dirname(__file__), "presets.json"), "r", encoding="utf-8"))

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

  def get_preset(self, name: str) -> dict:
    """ Returns a dictionary of the selected preset, key=name, value=size. """
    assert name in self._presets, f"Preset '{name}' does not exist."
    sizes = self._presets[name]
    preset = {}

    for size in sizes:
      name = size
      if ":" in size:
        size, name = size.split(":")[:2]
      preset[name] = tuple(map(int, size.split("x")[:2])) if "x" in size else (int(size), int(size))

    return preset

  def should_generate_all(self) -> bool:
    """ Returns True if all presets should be generated (default) """
    return not any([self._args[preset] for preset in PRESETS if preset in self._args])

  def should_generate_preset(self, preset: str) -> bool:
    """ Returns True if the specified preset should be generated. """
    assert preset in PRESETS, f"Preset '{preset}' does not exist."
    return self._args[preset] or self.should_generate_all()

  def create_preset_folder(self, preset: str) -> str:
    """ Creates a folder for the specified preset and returns the path. """
    assert preset in PRESETS, f"Preset '{preset}' does not exist."

    if not os.path.exists(self._output_path):
      os.mkdir(self._output_path)

    path = os.path.join(self._output_path, preset)
    os.mkdir(path)
    return path

  @property
  def img(self) -> Image:
    return self._img

  @property
  def org(self) -> Image:
    return self._org

  @property
  def name(self) -> str:
    return self._name

  @property
  def output_path(self) -> str:
    return self._output_path


if __name__ == "__main__":
  icon = CreateAppIcon()

  # Simple presets
  for preset in [Preset.IOS, Preset.APPLE_WATCH, Preset.IPAD, Preset.WEB]:
    if icon.should_generate_preset(preset.value):
      folder_path = icon.create_preset_folder(preset.value)
      for name, (w, h) in icon.get_preset(preset.value).items():
        img = icon.crop(w, h)
        img.save(os.path.join(folder_path, f"{name}.png"))
        # img = icon.resize(int(w), int(h), img=img)

  # if icon.should_generate_preset("web"):
  #   print("Nice")
  # else:
  #   print("Not generating web")
  # web_preset = icon.get_preset("web")
