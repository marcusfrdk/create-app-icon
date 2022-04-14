import shutil
import os
import numpy as np
from PIL import Image, ImageDraw
from typing import Union


PRESETS = ["apple_watch", "android", "web", "iphone", "ipad"]

    
def confirm(prompt: str) -> bool:
    """ Require user confirmation """
    if args.force and args.verbose:
        print("Force is enabled, ignoring confirmation...")
    return input(prompt).lower() in ["y", "ye", "yes"] if not args.force else True


def verbose(*msg) -> None:
    """ Print to console if verbose mode is enabled """
    if args.verbose:
        print(*msg)


def should_run_all() -> bool:
    """ Check if any preset if enabled """
    for preset in PRESETS:
        if getattr(args, preset):
            return False
    return True


def get_file_data(file_path: str) -> dict:
    """ Get image data from file """
    name, ext = file_path.split("/")[-1].split(".")[-2:]
    img = Image.open(file_path)
    path = os.path.abspath(file_path)
    w, h = img.size

    return {
        "width": w, 
        "height": h,
        "name": name,
        "type": ext,
        "path": path
    }


def resize_image(src: str, dst: str, width: int, height: int) -> None:
    name = dst.split("/")[-1]
    verbose(f"Resizing image '{name}'...")
    img = Image.open(src)
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(dst)


def round_image(src: str, dst: str, radius: int = None) -> None:
    # Get values
    img = Image.open(src).convert("RGB")
    w, h = img.size
    radius = radius if radius else max(h, w)
    name = dst.split("/")[-1]

    verbose(f"Rounding image '{name}'...")

    # Round image
    np_img = np.array(img)
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.rounded_rectangle(((0, 0), (h, w)), radius, 255)
    np_alpha = np.array(alpha)
    np_img = np.dstack((np_img, np_alpha))
    img = Image.fromarray(np_img)
    img.save(dst)


def get_dimensions(size: Union[int, str]) -> tuple:
    size = str(size)
    if "x" in size:
        w, h = size.split("x")
        return int(w), int(h)
    elif not size.isnumeric():
        raise TypeError("Invalid size")
    return int(size), int(size)


def crop_image(src: str, dst: str, cw: int = None, ch: int = None) -> None:
    """ Crop image to given size """
    img = Image.open(src)
    w, h = img.size
    name = dst.split("/")[-1]
    mx = my = min(w, h)

    if cw and ch:
        mx = cw
        my = ch

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
        bottom = h
        top = h - my

    verbose(f"Cropping '{name}'...")

    img = img.crop((left, top, right, bottom))
    img = img.resize((mx, my), Image.ANTIALIAS)
    img.save(dst)


def scale_image(src: str, dst: str, dim: int) -> None:
    """ Scale image to given size """
    img = Image.open(src)
    w, h = img.size
    sw, sh = w, h # (s)caled (w)idth and (s)caled (h)eight
    ratio = min(w, h) / max(w, h)
    name = dst.split("/")[-1]

    if w > h: # Landscape
        sw = dim
        sh = round(sw * ratio)
    else: # Portrait
        sh = dim
        sw = round(sh * ratio)

    verbose(f"Scaling '{name}' from {w}x{h} to {sw}x{sh}...")

    img = img.resize((sw, sh), Image.ANTIALIAS)
    img.save(dst)


def initialize() -> str:
    # Get values
    global output_folder_path
    global output_folder_created

    name = get_file_data(args.source)["name"]
    output_folder_path = os.path.join(os.getcwd(), "icons_" + name)
    output_folder_created = False
    all = should_run_all()
    
    # Create output root folder
    if os.path.exists(output_folder_path):
        if not args.force or args.verbose:
            print(f"The folder {output_folder_path} already exists.")
        if confirm("Do you want to overwrite it? (y/n) "):         
            verbose(f"Removing {output_folder_path}...")
            shutil.rmtree(output_folder_path)
        else:
            exit(0)

    # Generate remaining dirs
    verbose(f"Creating folder '{output_folder_path}'...")
    os.makedirs(output_folder_path)
    for preset in PRESETS:
        folder_path = os.path.join(output_folder_path, preset)
        if (getattr(args, preset) or all) and not os.path.exists(folder_path):
            verbose(f"Creating folder '{folder_path}'...")
            os.makedirs(folder_path)
    output_folder_created = True

    return output_folder_path


def clean(okay = False):
    if not okay:
        print("Aborting...")

        if output_folder_created:
            verbose(f"Removing {output_folder_path}...")
            shutil.rmtree(output_folder_path)
    
    tmp_sq_path = os.path.join(output_folder_path, "tmp-sq.png")
    tmp_org_path = os.path.join(output_folder_path, "tmp-org.png")
    os.remove(tmp_sq_path)
    os.remove(tmp_org_path)


def get_args() -> dict:
    """ Get arguments from command line """
    import argparse

    global args
    
    parser = argparse.ArgumentParser(description='Resize images to a given size.')
    parser.add_argument('source', type=str, help='path to source image')
    parser.add_argument("--iphone", help='generate iPhone icons', action="store_true")
    parser.add_argument("--ipad", help='generate iPad icons', action="store_true")
    parser.add_argument("--apple-watch", help='generate Apple Watch icons', action="store_true")
    parser.add_argument("--web", help='generate web icons', action="store_true")
    parser.add_argument("--android", help='generate Android icons', action="store_true")
    parser.add_argument("-v", "--verbose", help='show more output in terminal', action="store_true")
    parser.add_argument("-f", "--force", help='ignores any confirmations', action="store_true")
    parser.add_argument("--align-top", help='aligns the image to the top', action="store_true")
    parser.add_argument("--align-bottom", help='aligns the image to the bottom', action="store_true")
    args = parser.parse_args()

    # Check if source path exists and is valid
    valid_image_types = ["png", "jpg", "jpeg"]
    if not os.path.exists(args.source):
        print(f"The file '{args.source}' does not exist")
        exit(1)
    elif args.source.split(".")[-1] not in valid_image_types:
        print("Image must be of type:", ", ".join(valid_image_types))
        exit(1)

    return args
