import os
import json
from pickletools import optimize
import shutil
import numpy as np
import validators
import requests
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
    TAURI = "tauri"


class Icon(Enum):
    ICNS = "icns"
    ICO = "ico"


TEMPORARY_SIZE = 1024 # Size of temporary icon during processing
VALID_IMAGE_TYPES = ["png", "jpg", "jpeg"] # Image types known to work
VALID_CONTENT_TYPES = ["image/jpeg", "image/jpg", "image/png"]

favicon_sizes = [(x, x) for x in [16, 32, 48, 64, 128, 256, 512]]
default_icon_sizes = [(x, x) for x in [16, 32, 48, 64, 128, 256, 512]]
presets = [preset.value for preset in Preset]
sizes = json.load(open(os.path.join(os.path.dirname(__file__), "presets.json")))


def verbose(*msg) -> None:
    """ Prints a message to console only if verbose mode is enabled """
    if args.verbose: print(*msg)


def confirm(prompt: str) -> None:
    """ Require user confirmation """
    if args.force and args.verbose: print("Force is enabled, ignoring confirmation...")
    return input(prompt).lower() in ["y", "ye", "yes"] if not args.force else True


def get_file_name() -> str:
    """ Get the name of the file from a path """
    return src_path.split("/")[-1]


def get_size(size: Union[str, int]) -> tuple:
    """ Parse custom size format and return size and name """
    left, right = size.split(":") if ":" in size else (size, "")
    if "x" in left: w, h = tuple(map(int, left.split("x")))
    else: w = h = int(left)
    right = right + ".png" if right else f"{w}x{h}.png"
    return (w, h), right


def get_percent(value: float) -> float:
    """ Convert value to percentage """
    if not value or value < 0: return 0
    elif value > 100: return 1.0
    return value / 100


def is_url(url: str) -> bool:
    """ Cheks if a string is a valid URL """
    try: return validators.url(url)
    except validators.ValidationFailure: return False


def get_output_folder_path() -> str:
    """ Get the name of the output directory """
    if args.output:
        return args.output
    elif is_remote:
        return "output_remote_" + str(round(time.time()))
    return "output_" + os.path.abspath(args.source).split("/")[-1].split(".")[0]


def get_src_path() -> str:
    """ Get the source path from the command line """
    return remote_path if is_remote else os.path.abspath(args.source)


def resize_image(img: Image, w: int, h: int) -> Image:
    """ Resize image to given size """
    name = get_file_name()
    verbose(f"Resizing image {name} to {w}x{h}...")
    return img.resize((w, h), Image.ANTIALIAS)


def scale_image(img: Image, max_size: int) -> Image:
    """ Scale image to given size """
    w, h = img.size
    sw, sh = w, h # (s)caled (w)idth and (s)caled (h)eight
    should_upscale = max_size > min(w, h)
    ratio = max(w, h) / min(w, h) if should_upscale else min(w, h) / max(w, h)
    name = get_file_name()

    if should_upscale: # Upscale
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
        mx, my = nw, nh

    left = (w - mx)/2
    top = (h - my)/2
    right = (w + mx)/2
    bottom = (h + my)/2

    if args.top:
        verbose("Image alignment set to 'top'")
        top, bottom = 0, my
    elif args.bottom:
        verbose("Image alignment set to 'bottom'")
        top, bottom = h - my, h
    elif args.offset:
        verbose(f"Image alignment set to custom, offset set to {args.offset} pixels")
        top, bottom = top + args.offset, bottom + args.offset
    
    verbose(f"Cropping '{name}'...")
    img = img.crop((left, top, right, bottom))
    return img.resize((mx, my), Image.ANTIALIAS)


def round_image(img: Image, radius: int) -> Image:
    """ Round image corners """
    img = img.convert("RGB")
    w, h = img.size
    radius = radius if radius else max(h, w)
    np_img = np.array(img)
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.rounded_rectangle(((0, 0), (h, w)), radius, 255)
    np_alpha = np.array(alpha)
    np_img = np.dstack((np_img, np_alpha))
    return Image.fromarray(np_img)


def generate_image(folder_path: str, size: str):
    """ Generate icon and saves it """
    (w, h), name = get_size(size)
    if w != h: 
        img = crop_image(scale_image(Image.open(org_path), max(w, h)), w, h)
    else:
        img = resize_image(Image.open(sq_path), w, h)
    img.save(os.path.join(folder_path, name))


def generate_android_icons() -> None:
    """ Custom generation function for Android icons """
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

# Should this be combined with "generate_icon()" maybe?
def generate_favicon(path: str) -> None:
    """ Custom generation function for favicon """
    favicon_path = os.path.join(path, "favicon.ico")
    img = Image.open(sq_path)
    pct = get_percent(args.favicon_radius)
    if pct <= 0:
        verbose("Favicon radius is invalid, skipping favicon rounding...")
    elif args.favicon_radius:
        verbose(f"Rounding favicon by {int(100 * pct)}%")
        img = round_image(img, max(img.size) * pct)
    img.save(favicon_path, format="ICO", optimize=True, icc_profile=None, sizes=favicon_sizes)
    verbose("Favicon successfully generated")


def generate_icon(path: str, file_type: Icon, name: str = "icon", sizes = default_icon_sizes) -> None:
    file_name = f"{name}.{file_type.value}"
    output_path = os.path.join(path, file_name)
    img = Image.open(sq_path)
    percent = get_percent(args.icon_radius)
    if percent > 0:
        verbose(f"Rounding {file_name} by {int(percent) * 100}%")
        img = round_image(img, max(img.size) * percent)
    img.save(output_path, format=file_type.value, optimize=True, sizes=sizes)
    verbose(f"{file_name} successfully generated")


def generate_manifest() -> None:
    """ Created manifest file for web """
    manifest_path = os.path.join(web_path, "manifest.json")
    icons = []
    for size in sizes[Preset.WEB.value]:
        (w, h), name = get_size(size)
        icons.append({"src": f"{name}", "sizes": f"{w}x{h}", "type": "image/png"})

    icons.append({
        "src": "favicon.ico",
        "sizes": " ".join([f"{size[0]}x{size[1]}" for size in favicon_sizes]).strip(),
        "type": "image/x-icon"
    })

    manifest = {
        "short_name": "Your App's Name",
        "name": "Your App's Name",
        "theme_color": "#ffffff",
        "background_color": "#ffffff",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait",
        "icons": icons
    }

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)

    verbose("Manifest successfully generated")


def fetch() -> None:
    """ Fetch image from URL """
    response = requests.get(args.source)
    content_type = response.headers.get("Content-Type")
    
    if not content_type.lower() in VALID_CONTENT_TYPES:
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
    """ Initialize program and created required folders and files """
    global created_by_program
    # Create temporary files
    if not is_remote:
        # Make sure src is valid
        if not os.path.exists(src_path):
            print(f"The file '{src_path}' does not exist")
            exit(1)
        elif src_path.split(".")[-1].lower() not in VALID_IMAGE_TYPES:
            print("Image must be of type:", ", ".join(VALID_IMAGE_TYPES))
            exit(1)

    # Create output root folder
    if os.path.exists(output_path):
        folder_name = output_path.split("/")[-1]
        if not confirm(f"Folder '{folder_name}' already exists. Do you want to overwrite it? (y/n) "):
            exit(0)
        else:
            shutil.rmtree(output_path)
    verbose("Creating", output_path)
    os.makedirs(output_path)
    created_by_program = True

    # Create remaining folders
    for preset in presets:
        if getattr(args, preset) or all:
            folder_path = os.path.join(output_path, preset)
            verbose("Creating", folder_path)
            os.makedirs(folder_path)

    # Download remote
    if is_remote:
        print(f"Downloading {args.source}...")
        fetch()
    
    # Create temporary images
    print("Generating icons...")
    shutil.copyfile(src_path, original_path)
    scale_image(Image.open(original_path), TEMPORARY_SIZE).save(org_path)
    crop_image(Image.open(org_path)).save(sq_path)
    verbose("Temporary icons created...")


def clean(error: bool = False) -> None:
    """ Clean up temporary files and folders """
    files_to_remove = [org_path, sq_path, remote_path]
    if isinstance(created_by_program, bool) and created_by_program and error:
        print("Something went wrong, cleaning up...")
        verbose(f"Removing {output_path}...")
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
    parser.add_argument('source', type=str, help='path to source image', nargs="?")
    parser.add_argument("-v", "--verbose", help='show more output in terminal', action="store_true")
    parser.add_argument("-f", "--force", help='ignores any confirmations', action="store_true")
    parser.add_argument("-o", "--output", help='name of the output folder', type=str)
    parser.add_argument("--iphone", help='generate iPhone icons', action="store_true")
    parser.add_argument("--tauri", help='generate Tauri icons', action="store_true")
    parser.add_argument("--ipad", help='generate iPad icons', action="store_true")
    parser.add_argument("--apple-watch", help='generate Apple Watch icons', action="store_true")
    parser.add_argument("--web", help='generate web icons', action="store_true")
    parser.add_argument("--android", help='generate Android icons', action="store_true")
    parser.add_argument("--top", help='aligns the image to the top', action="store_true")
    parser.add_argument("--bottom", help='aligns the image to the bottom', action="store_true")
    parser.add_argument("--offset", help='offsets the alignment from the center', type=int)
    parser.add_argument("--favicon-radius", help='sets the border radius of the favicon as a percentage', type=int, const=15, nargs="?")
    parser.add_argument("--icon-radius", help='sets the border radius of the icon(s) as a percentage', type=int, const=0, nargs="?")
    return parser.parse_args()


def main() -> None:
    """ Main function """

    global args
    global src_path
    global org_path
    global sq_path
    global remote_path
    global original_path
    global output_path
    global web_path
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
    web_path = os.path.join(output_path, Preset.WEB.value)
    run_all = should_run_all_presets()
    created_by_program = False # output folder created by this program

    try:
        initialize()

        # Simple presets
        for preset in [p for p in presets if p not in [Preset.ANDROID.value, Preset.WEB.value, Preset.TAURI.value]]:
            if getattr(args, preset) or run_all:
                for size in sizes[preset]:
                    generate_image(os.path.join(output_path, preset), size)

        # Custom presets
        if args.android or run_all:
            generate_android_icons()

        # Web preset
        if args.web or run_all:
            web_path = os.path.join(output_path, Preset.WEB.value)
            for size in sizes[Preset.WEB.value]:
                generate_image(web_path, size)
            generate_favicon(web_path)
            generate_manifest()
        
        # Tauri preset
        if args.tauri or run_all:
            tauri_path = os.path.join(output_path, Preset.TAURI.value)
            for size in sizes[Preset.TAURI.value]:
                generate_image(tauri_path, size)
            generate_favicon(tauri_path)
            generate_icon(tauri_path, Icon.ICO, "icon")
            generate_icon(tauri_path, Icon.ICNS, "icon")

        print(f"Successfully generated icons in {output_path}")
        clean()
    except:
        clean(True)
        if args.verbose:
            print_exc()


if __name__ == "__main__":
    main()
