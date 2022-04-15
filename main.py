import os
import json
import shutil
import numpy as np
import validators
import requests
import datetime
import time
from PIL import Image, ImageDraw
from typing import Union
from enum import Enum
from argparse import ArgumentParser
from traceback import print_exc

class Preset(Enum):
    IPHONE = "iphone"
    IPAD = "ipad"
    ANDROID = "android"
    APPLE_WATCH = "apple_watch"
    WEB = "web"


VERBOSE = False
FORCE = False
DEFAULT_PATH = os.path.abspath(os.path.join(os.getcwd(), "images", "landscape.jpg"))
DEFAULT_SIZE = 1024
VALID_IMAGE_TYPES = ["png", "jpg", "jpeg"]
VALID_CONTENT_TYPES = ["image/jpeg", "image/jpg", "image/png"]

presets = [preset.value for preset in Preset]
sizes = json.load(open(os.path.join(os.path.dirname(__file__), "presets.json")))


def verbose(*msg) -> None: 
    if args.verbose: print(*msg)


def confirm(prompt: str) -> None:
    """ Require user confirmation """
    if args.force and args.verbose:
        print("Force is enabled, ignoring confirmation...")
    return input(prompt).lower() in ["y", "ye", "yes"] if not args.force else True


def get_file_name() -> str:
    return src_path.split("/")[-1]


def get_size(size: Union[str, int]) -> tuple:
    left, right = size.split(":") if ":" in size else (size, "")
    if "x" in left: w, h = tuple(map(int, left.split("x")))
    else: w = h = int(left)
    if right:
        right = right + ".png"
    else:
        right = f"{w}x{h}.png"
    
    return (w, h), right


def get_percent(value: int) -> float:
    if value > 100: return 1.0
    elif value < 0: return 0.0
    return value / 100


def is_url(url: str) -> bool:
    try: return validators.url(url)
    except validators.ValidationFailure: return False


def get_output_folder_path() -> str:
    """ Get the name of the output directory """
    if is_remote:
        return "output_remote_" + str(round(time.time()))
    return "output_" + os.path.abspath(args.source).split("/")[-1].split(".")[0]


def get_src_path() -> str:
    if is_remote: return remote_path
    return os.path.abspath(args.source)


def resize_image(img: Image, w: int, h: int) -> Image:
    name = get_file_name()
    verbose(f"Resizing image {name} to {w}x{h}...")
    return img.resize((w, h), Image.ANTIALIAS)


def scale_image(img: Image, max_size: int) -> Image:
    """ Scale image to given size """
    w, h = img.size
    sw, sh = w, h # (s)caled (w)idth and (s)caled (h)eight
    ratio = min(w, h) / max(w, h)
    name = get_file_name()

    if max_size > min(w, h): # Upscale
        ratio = max(w, h) / min(w, h)
        diff = (max_size, round(max_size * ratio)) if w < h else (round(max_size * ratio), max_size)
        verbose(f"Upscaling '{name}' from {w}x{h} to {diff[0]}x{diff[1]}...")
        return img.resize(diff, Image.ANTIALIAS)
    else: # Downscale
        if w > h: # Landscape
            sw = max_size
            sh = round(sw * ratio)
        else: # Portrait
            sh = max_size
            sw = round(sh * ratio)

        verbose(f"Downscaling '{name}' from {w}x{h} to {sw}x{sh}...")

        return img.resize((sw, sh), Image.ANTIALIAS)


def crop_image(img: Image, nw: int = None, nh: int = None) -> Image:
    """ Crop image to given size """
    w, h = img.size
    mx = my = min(w, h)
    name = get_file_name()

    if nw and nh:
        mx = nw
        my = nh

    left = (w - mx)/2
    top = (h - my)/2
    right = (w + mx)/2
    bottom = (h + my)/2

    if args.align_top:
        verbose("Image alignment set to 'top'")
        top = 0
        bottom = my
    elif args.align_bottom:
        verbose("Image alignment set to 'bottom'")
        top = h - my
        bottom = h
    elif args.align_offset:
        verbose(f"Image alignment set to custom, offset set to {args.align_offset} pixels")
        top = top + args.align_offset
        bottom = bottom + args.align_offset

    verbose(f"Cropping '{name}'...")

    img = img.crop((left, top, right, bottom))
    return img.resize((mx, my), Image.ANTIALIAS)


def round_image(img: Image, radius: int) -> Image:
    # Get values
    img = img.convert("RGB")
    w, h = img.size
    radius = radius if radius else max(h, w)
    name = get_file_name()

    verbose(f"Rounding image '{name}'...")

    # Round image
    np_img = np.array(img)
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.rounded_rectangle(((0, 0), (h, w)), radius, 255)
    np_alpha = np.array(alpha)
    np_img = np.dstack((np_img, np_alpha))

    return Image.fromarray(np_img)


def generate_icon(folder_path: str, size: str):
    (w, h), name = get_size(size)
    if w != h:
        img = crop_image(scale_image(Image.open(org_path), max(w, h)), w, h)
    else:
        img = resize_image(Image.open(sq_path), w, h)
    img.save(os.path.join(folder_path, name))


def generate_android_icons() -> None:
    android_path = os.path.join(output_path, "android")
    for size in sizes[Preset.ANDROID.value]:
        (w, h), folder_name = get_size(size)
        folder_name = folder_name.replace(".png", "")
        folder_path = os.path.join(android_path, folder_name)
        os.makedirs(folder_path)
        ic_path = os.path.join(folder_path, "ic_launcher.png")
        resize_image(Image.open(sq_path), w, h).save(ic_path)
        if folder_name != "play_store":
            icr_path = os.path.join(folder_path, "ic_launcher_round.png")
            round_image(resize_image(Image.open(sq_path), w, h), max(w, h)).save(icr_path)


def generate_favicon() -> None:
    favicon_path = os.path.join(output_path, Preset.WEB.value, "favicon.ico")
    favicon_layers = [(x, x) for x in [16, 32, 48, 64, 128, 256, 512]]
    img = Image.open(sq_path)
    pct = get_percent(args.favicon_radius)
    if pct <= 0:
        verbose("Favicon radius is invalid, skipping favicon rounding...")
    elif args.favicon_radius:
        verbose(f"Rounding favicon by {int(100 * pct)}%")
        img = round_image(img, max(img.size) * pct)
    img.save(favicon_path, format="ICO", optimize=True, icc_profile=None, sizes=favicon_layers)
    verbose("Favicon successfully generated")


def fetch() -> None:
    response = requests.get(args.source)
    content_type = response.headers.get("Content-Type")
    
    if not content_type in VALID_CONTENT_TYPES:
        print(f"The content type '{content_type}' is currently not supported.")
        exit(1)

    with open(src_path, "wb+") as file:
        file.write(response.content)

    verbose("Succefully downloaded image")


def should_run_all_presets() -> bool:
    """ Check if any preset are enabled """
    for preset in presets:
        if getattr(args, preset):
            return False
    return True


def initialize():
    # Create output root folder
    if os.path.exists(output_path):
        folder_name = output_path.split("/")[-1]
        if not confirm(f"Folder '{folder_name}' already exists. Do you want to overwrite it? (y/n) "):
            exit(0)
        else:
            shutil.rmtree(output_path)
    verbose("Creating", output_path)
    os.makedirs(output_path)

    # Create remaining folders
    for preset in presets:
        if getattr(args, preset) or all:
            folder_path = os.path.join(output_path, preset)
            verbose("Creating", folder_path)
            os.makedirs(folder_path)

    # Create temporary files
    if is_remote:
        print(f"Downloading {args.source}...")
        fetch()
    else:
        print("Generating icons...")
        # Make sure src is valid
        if not os.path.exists(src_path):
            print(f"The file '{src_path}' does not exist")
            exit(1)
        elif src_path.split(".")[-1].lower() not in VALID_IMAGE_TYPES:
            print("Image must be of type:", ", ".join(VALID_IMAGE_TYPES))
            exit(1)
    
    # Create temporary images
    shutil.copyfile(src_path, original_path)
    scale_image(Image.open(original_path), DEFAULT_SIZE).save(org_path)
    crop_image(Image.open(org_path)).save(sq_path)


def clean(error: bool = False) -> None:
    files_to_remove = [org_path, sq_path, remote_path]
    if isinstance(created_by_program, bool) and created_by_program and error:
        verbose("Output path created by program, removing...")
        shutil.rmtree(output_path, ignore_errors=True)
    else:
        # Remove temporary files
        for file in files_to_remove:
            if os.path.exists(file):
                verbose(f"Removing temporary file {file}...")
                os.remove(file)

        # Remove empty directories
        for path, dirs, files in os.walk(output_path):
            if len(os.listdir(path)) == 0:
                verbose(f"Removing empty directory {path}...")
                os.rmdir(path)


def get_args() -> dict:
    """ Get arguments from command line """
    parser = ArgumentParser(description='Resize an image to multiple sizes and formats at once.')
    parser.add_argument('source', type=str, help='path to source image', nargs="?", default=DEFAULT_PATH)
    parser.add_argument("--iphone", help='generate iPhone icons', action="store_true")
    parser.add_argument("--ipad", help='generate iPad icons', action="store_true")
    parser.add_argument("--apple-watch", help='generate Apple Watch icons', action="store_true")
    parser.add_argument("--web", help='generate web icons', action="store_true")
    parser.add_argument("--android", help='generate Android icons', action="store_true")
    parser.add_argument("-v", "--verbose", help='show more output in terminal', action="store_true", default=VERBOSE)
    parser.add_argument("-f", "--force", help='ignores any confirmations', action="store_true", default=FORCE)
    parser.add_argument("--align-top", help='aligns the image to the top', action="store_true")
    parser.add_argument("--align-bottom", help='aligns the image to the bottom', action="store_true")
    parser.add_argument("--align-offset", help='offsets the alignment from the center', type=int)
    parser.add_argument("--favicon-radius", help='sets the border radius of the favicon as a percentage', type=int)
    return parser.parse_args()


def main() -> None:
    global args
    global src_path
    global org_path
    global sq_path
    global remote_path
    global original_path
    global output_path
    global created_by_program
    global is_remote

    args = get_args()
    is_remote = is_url(args.source)
    output_path = get_output_folder_path()
    remote_path = os.path.join(output_path, "tmp-remote.png")
    src_path = get_src_path()
    org_path = os.path.join(output_path, "tmp-org.png")
    sq_path = os.path.join(output_path, "tmp-sq.png")
    original_path = os.path.join(output_path, "original.png")
    run_all = should_run_all_presets()
    created_by_program = False
    
    try:
        initialize()
        created_by_program = True

        # Simple presets
        for preset in [p for p in presets if p not in [Preset.ANDROID.value, Preset.WEB.value]]:
            if getattr(args, preset) or run_all:
                for size in sizes[preset]:
                    generate_icon(os.path.join(output_path, preset), size)

        # Custom presets
        if args.android or run_all:
            generate_android_icons()

        # Remaining web
        if args.web or run_all:
            for size in sizes[Preset.WEB.value]:
                generate_icon(os.path.join(output_path, Preset.WEB.value), size)
            generate_favicon()

        print(f"Successfully generated icons in {output_path}")

        clean()
    except:
        clean(True)
        if args.verbose:
            print_exc()


if __name__ == "__main__":
    main()
