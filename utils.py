import platform
import os
from config import FILE_TYPE, OUTPUT_FOLDER_NAME

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
    output_folder_name = OUTPUT_FOLDER_NAME + "-" + file_name
    return os.path.abspath(os.path.join(caller_path, output_folder_name))

def get_image_path(image_path: str) -> str:
    if not image_path or not os.path.exists(image_path):
        print("Image does not exist")
        exit(0)
    return image_path
