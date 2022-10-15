import argparse
import io
import json
import os
import time
from enum import Enum

import numpy as np
import requests
import validators
from PIL import Image, ImageDraw

FETCH_FILE_PATH = os.path.join(os.getcwd(), ".create-app-icon.png")
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
  parser.add_argument(
    "-r",
    "--radius",
    help="sets the border radius of the favicon.",
    type=int,
    default=0,
    action=RadiusAction
  )
  parser.add_argument(
    "-a",
    "--align",
    help="aligns the image in x and/or y.",
    type=str,
    choices=["top", "right", "bottom", "left"],
    action=AlignAction,
    nargs="+"
  )

  return vars(parser.parse_args())


class PathAction(argparse.Action):
  """ Formats the input path, if path is url, it will download the image. """

  def __call__(self, parser, namespace, values, option_string=None):
    if validators.url(values):
      response = requests.get(values, allow_redirects=False)
      content_type = response.headers.get("Content-Type")

      if response.status_code != 200:
        raise requests.RequestException(f"Failed to get url with status code {response.status_code}.")

      if not content_type.lower().startswith("image/"):
        raise ValueError(f"Url '{values}' does not point to an image.")

      values = FETCH_FILE_PATH
      Image.open(io.BytesIO(response.content)).convert("RGBA").save(values, format="png")
    else:
      if not os.path.exists(values):
        raise FileNotFoundError(f"File '{values}' does not exist.")
    setattr(namespace, self.dest, values)


class AlignAction(argparse.Action):
  """ Makes sure that the align argument is valid. """

  def __call__(self, parser, namespace, values, option_string=None):
    if len(values) > 2:
      raise ValueError("You can only specify 2 alignments.")
    if "top" in values and "bottom" in values:
      raise ValueError("Top- and bottom alignments are exclusive.")
    if "left" in values and "right" in values:
      raise ValueError("Left- and right alignments are exclusive.")
    setattr(namespace, self.dest, values)


class RadiusAction(argparse.Action):
  """ Makes sure the radius is a percentage. """

  def __call__(self, parser, namespace, values, option_string=None):
    if values < 0 or values > 100:
      raise ValueError("Radius must be a percentage (0-100)")
    setattr(namespace, self.dest, values)


class CreateAppIcon():
  """ 
    Main class for generating icons. The purpose of the class is 
    to load the image and initialize the presets.

    All the user has to do is to call the methods they want based
    on the stored input image.
  """

  def __init__(self):
    self._args = get_args()
    self._name = os.path.splitext(os.path.basename(self._args["path"]))[
        0] if FETCH_FILE_PATH != self._args["path"] else "fetch"
    self._output_path = os.path.join(os.getcwd(), f"output-{self._name}-{int(time.time())}")
    self._presets = json.load(open(os.path.join(os.path.dirname(__file__), "presets.json"), "r", encoding="utf-8"))

    self._org = Image.open(self._args["path"]).convert("RGBA")
    self._img = self.crop(1024, img=self.rescale(2048 if self._args["align"] else 1024, img=self._org))

  def crop(
      self,
      width: int = None,
      height: int = None,
      img: Image.Image = None
  ) -> Image.Image:
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

    return img.crop((left, top, right, bottom)).resize((mx, my), Image.Resampling.LANCZOS)

  def rescale(self, max_size: int, img: Image.Image = None) -> Image.Image:
    """ Rescale the image with the largest size equal to 'max_size'. """
    img = img if img else self._img
    w, h = img.size

    if max_size > min(w, h):
      # Upscale image
      ratio = max(w, h) / min(w, h)
      width = max_size if w < h else round(max_size * ratio)
      height = round(max_size * ratio) if w < h else max_size
      return img.resize((width, height), Image.Resampling.LANCZOS)

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

    return img.resize((width, height), Image.Resampling.LANCZOS)

  def resize(self, width: int, height: int = None, img: Image.Image = None) -> Image.Image:
    """ Resize the image to the specified width and height. """
    img = img if img else self._img
    height = height if height else width
    return img.resize((width, height), Image.Resampling.LANCZOS)

  def round(self, radius: int = None, img: Image.Image = None) -> Image.Image:
    """ Rounds an image with the specified radius, defaults to fully rounded. """
    if radius:
      assert radius >= 0 and radius <= 100, "Radius must be a percentage (0-100)"

    img = (img if img else self._img).convert("RGB")
    w, h = img.size
    percentage = (radius if radius else self._args["radius"] if self._args["radius"] else 0) / 100
    radius = max(img.size) * percentage if percentage else max(img.size)
    np_img = np.array(img)
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.rounded_rectangle(((0, 0), (h, w)), radius, 255)
    np_alpha = np.array(alpha)
    np_img = np.dstack((np_img, np_alpha))
    return Image.fromarray(np_img)

  def generate_favicon(self) -> None:
    """ Returns an image with the size of a favicon, you still have to save it as a favicon. """
    path = os.path.join(self.get_preset_folder_path(Preset.WEB), "favicon.ico")
    sizes = [(x, x) for x in [16, 32, 48, 64, 128, 256, 512]]
    img = self.rescale(512)
    img = self.crop(512, 512, img=img)
    img = self.round(img=img)
    img.save(path, format="ICO", optimize=True, icc_profile=None, sizes=sizes)

  def get_preset(self, preset: Preset) -> dict:
    """ Returns a dictionary of the selected preset, key=name, value=size. """
    assert preset.value in self._presets, f"Preset '{name}' does not exist."
    sizes = self._presets[preset.value]
    output = {}

    for size in sizes:
      name = size
      if ":" in size:
        size, name = size.split(":")[:2]
      output[name] = tuple(map(int, size.split("x")[:2])) if "x" in size else (int(size), int(size))

    return output

  def should_generate_all(self) -> bool:
    """ Returns True if all presets should be generated (default) """
    return not any([self._args[preset] for preset in PRESETS if preset in self._args])

  def should_generate_preset(self, preset: Preset) -> bool:
    """ Returns True if the specified preset should be generated. """
    assert isinstance(preset, Preset), f"Preset '{preset}' is invalid."
    return self._args[preset.value] or self.should_generate_all()

  def create_preset_folder(self, preset: Preset) -> str:
    """ Creates a folder for the specified preset and returns the path. """
    assert isinstance(preset, Preset), f"Preset '{preset}' is invalid."

    if not os.path.exists(self._output_path):
      os.mkdir(self._output_path)

    path = os.path.join(self._output_path, preset.value)
    os.mkdir(path)
    return path

  def get_preset_folder_path(self, preset: Preset) -> str:
    """ Returns the path to the preset folder. """
    assert isinstance(preset, Preset), f"Preset '{preset}' is invalid."
    return os.path.join(self._output_path, preset.value)

  def cleanup(self) -> None:
    """ Cleanup function that removes temporary files. """

    # Remove tmp fetch image
    if os.path.exists(FETCH_FILE_PATH):
      os.remove(FETCH_FILE_PATH)

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
    if icon.should_generate_preset(preset):
      folder_path = icon.create_preset_folder(preset)
      for name, (w, h) in icon.get_preset(preset).items():
        if w != h:
          img = icon.rescale(max(w, h))
          img = icon.crop(w, h, img=img)
        else:
          img = icon.resize(w, h)
        img.save(os.path.join(folder_path, f"{name}.png"))

  # Web (extra) (favicon)
  if icon.should_generate_preset(Preset.WEB):
    icon.generate_favicon()

  # Android
  if icon.should_generate_preset(Preset.ANDROID):
    folder_path = icon.create_preset_folder(Preset.ANDROID)
    for name, (w, h) in icon.get_preset(Preset.ANDROID).items():
      subfolder_path = os.path.join(folder_path, name)
      os.mkdir(subfolder_path)

      img = icon.rescale(max(w, h))
      img = icon.crop(w, h, img=img)

      imgr = icon.round(icon._args["radius"], img=img)

      img.save(os.path.join(subfolder_path, f"ic_launcher.png"))
      imgr.save(os.path.join(subfolder_path, f"ic_launcher_round.png"))

  # Cleanup
  print(f"Output saved to {icon.output_path}")
  icon.cleanup()
