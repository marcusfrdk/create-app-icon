import os
import json
import shutil
import numpy as np
from PIL import Image, ImageDraw
from typing import Union
from enum import Enum
from argparse import ArgumentParser
from traceback import print_exc


class Preset(Enum):
    iphone = "iphone"
    ipad = "ipad"
    android = "android"
    apple_watch = "apple_watch"
    web = "web"


VERBOSE = False
FORCE = True
PRESETS = [preset.value for preset in Preset]
DEFAULT_PATH = os.path.abspath(os.path.join(os.getcwd(), "images", "landscape.jpg"))


def verbose(*msg) -> None: 
    if args.verbose: print(*msg)


def confirm(prompt: str) -> None:
    """ Require user confirmation """
    if args.force and args.verbose:
        print("Force is enabled, ignoring confirmation...")
    return input(prompt).lower() in ["y", "ye", "yes"] if not args.force else True


def get_file_data(img: Image) -> tuple:
    return img.filename.split(".") # name, extension


def get_output_folder_path() -> str:
    """ Get the name of the output directory """
    folder_name = "output_" + src_path.split("/")[-1].split(".")[0]
    return os.path.abspath(os.path.join(os.getcwd(), folder_name))


def parse_size(size: Union[str, int]) -> tuple:
    if not str(size).replace("x", "").isnumeric():
        verbose(f"Invalid size format {size}")
        return (0, 0)
    if "x" in str(size):
        return tuple(map(int, size.split("x")))
    return (int(size), int(size))


def validate_src() -> bool:
    valid_image_types = ["png", "jpg", "jpeg"]
    if not os.path.exists(src_path):
        print(f"The file '{src_path}' does not exist")
        exit(1)
    elif src_path.split(".")[-1].lower() not in valid_image_types:
        print("Image must be of type:", ", ".join(valid_image_types))
        exit(1)


def initialize() -> bool:
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
    for preset in PRESETS:
        if getattr(args, preset) or all:
            folder_path = os.path.join(output_path, preset)
            verbose("Creating", folder_path)
            os.makedirs(folder_path)

    return True


def clean(exception: bool = False) -> None:
    print("EXCEPTION", exception, "#################")
    print("CREATED", created)

    files_to_remove = [org_path, sq_path]
    if isinstance(created, bool) and created:
        verbose("Output path created by program, removing...")
        shutil.rmtree(output_path, ignore_errors=True)
    else:
        for file in files_to_remove:
            if os.path.exists(file):
                verbose(f"Removing {file}...")
                os.remove(file)


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
    return parser.parse_args()


def main() -> None:
    global args
    global src_path
    global org_path
    global sq_path
    global output_path
    global created

    args = get_args()
    src_path = os.path.abspath(args.source)
    org_path = os.path.join(src_path, "tmp-org.png")
    sq_path = os.path.join(src_path, "tmp-sq.png")
    output_path = get_output_folder_path()
    created = False

    validate_src()
    
    try:
        created = initialize()
        clean()
    except:
        if args.verbose:
            print_exc()
        clean(True)
        pass


if __name__ == "__main__":
    main()
