import platform
import os
import validators
from datetime import datetime
from validators.utils import ValidationFailure
from config import FILE_TYPE, OUTPUT_FOLDER_NAME
from fetch import fetch_image

def get_file_name(file: str) -> str:
    name = file
    if ":" in file:
        name = file.split(":")[1]
    return f"{name}.{FILE_TYPE}"


def get_file_size(file: str, as_string: bool = False) -> str:
    if ":" in file:
        dim = file.split(":")[0]
        if as_string:
            return dim
        elif "x" in dim:
            dim = dim.split("x")[0]
            h = dim[0]
            w = dim[1]
            return (h, w)
        else:
            return file
    else:
        return file


def is_file(key: str) -> bool:
    if "x" in key:
        key = key.split("x")[0]
        return key.isnumeric()
    return False


def is_rounded(key: str) -> bool:
    return ":rounded" in key


def get_categories(args):
    categories = []
    if args.web:
        categories.append("web")
    if args.android:
        categories.append("android")
    if args.apple_watch:
        categories.append("apple_watch")
    if args.ios:
        categories.append("ios")

    if not args.ios and not args.web and not args.android and not args.apple_watch:
        categories = ["web", "ios", "apple_watch", "android"]
    
    return categories


def get_path_separator() -> str:
    if platform.system == "Windows":
        return "\\"
    return "/"


def get_output_path(image_path: str, custom_name: str = None):
    if custom_name:
        return custom_name

    separator = get_path_separator()
    file_name = image_path.split(separator)[-1].split(".")[0]
    caller_path = os.getcwd()
    output_folder_name = OUTPUT_FOLDER_NAME + "-" + (file_name if not is_url(image_path) else "fetch")
    return os.path.abspath(os.path.join(caller_path, output_folder_name))


def is_url(url: str) -> bool:
    try:
        return validators.url(url)
    except ValidationFailure:
        return False


def get_output_folder_path(image_path: str, custom_name: str = "", fetch_name: str = "") -> str:
    caller_path = os.getcwd()
    folder_name = OUTPUT_FOLDER_NAME + "-"

    if is_url(image_path):
        folder_name = folder_name + fetch_name
    elif custom_name:
        folder_name = custom_name
    else:
        image_path = image_path.replace("-tmp", "")
        folder_name = folder_name + os.path.basename(image_path).split(".")[0]

    return os.path.abspath(os.path.join(caller_path, folder_name))


def get_fetch_name() -> str:
    return f"fetch-{datetime.now().microsecond}"


def clean(image_path: str, args) -> None:
    os.remove(image_path)
    print("Removed temporary file")


def get_image_name(image_path: str) -> str:
    return os.path.basename(image_path)

