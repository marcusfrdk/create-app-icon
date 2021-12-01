import shutil
import os
import config
import json
from typing import Union
from fetch import fetch_image
from utils import get_file_name, get_file_size, is_file, is_rounded, is_url
from PIL import Image
from transform import square_image, resize_image, round_image

def create_manifest(output_path: str) -> Union[dict, None]:
    if config.GENERATE_MANIFEST:
        web_icons = [icon[0] for icon in list(config.SIZES.get("web").items()) if icon[1]]
        icons = [{
            "src": f"{config.OUTPUT_FOLDER_NAME}/{get_file_name(icon)}",
            "sizes": get_file_size(icon, True),
            "type": f"image/{config.FILE_TYPE.lower()}"
        } for icon in web_icons]

        if config.GENERATE_FAVICON:
            icons.append({
                "src": f"{config.OUTPUT_FOLDER_NAME}/favicon.ico",
                "sizes": " ".join([f"{size[0]}x{size[1]}" for size in config.FAVICON_SIZES]).strip(),
                "type": "image/x-icon"
            })

        manifest = {
            "theme_color": config.MANIFEST_THEME_COLOR,
            "background_color": config.MANIFEST_BACKGROUND_COLOR,
            "display": config.MANIFEST_DISPLAY,
            "scope": config.MANIFEST_SCOPE,
            "start_url": config.MANIFEST_START_URL,
            "icons": icons
        }

        manifest_path = os.path.join(output_path, "manifest.json")
        create_file(manifest_path, json.dumps(manifest, indent=4, sort_keys=True))
        print("Manifest created")
        return manifest
    else:
        print("Ignoring manifest...")


def create_html_tags(output_path: str, manifest: Union[dict, None]) -> None:
    if manifest:
        theme_color = config.MANIFEST_THEME_COLOR

        static_tags = ['<meta name="apple-mobile-web-app-status-bar-style" content="default" />',
            '<meta name="msapplication-config" content="none" />',
            f'<meta name="apple-mobile-web-app-status-bar-title" content="{config.MANIFEST_NAME}" />',
            f'<meta name="theme-color" content="{theme_color}" />',
            f'<meta name="msapplication-TileColor" content="{theme_color}" />',]

        if config.GENERATE_FAVICON:
            static_tags.append('<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />')

        dynamic_tags = []
        for icon in manifest.get("icons"):
            name = icon["src"].replace(config.OUTPUT_FOLDER_NAME, "")[1:].split(".")[0]
            if not is_file(name) and name != "favicon":
                dynamic_tags.append(f'<link rel="{name}" href="{icon["src"]}" type="image/png" />')

        html_tags = static_tags + dynamic_tags
        html_path = os.path.join(output_path, "tags.html")

        with open(html_path, "w+", encoding="utf-8") as file:
            file.write("\n".join(html_tags).strip())

        print("HTML tag file created")


def create_favicon(output_path: str, image_path: str, radius: str = None) -> None:
    if config.GENERATE_FAVICON:
        favicon_path = os.path.join(output_path, "favicon.ico")
        img = Image.open(image_path)
        img = square_image(img)
        if radius:
            print("Rounding favicon with radius", radius)
            img = round_image(img, int(radius) if radius and radius.isnumeric() else 0)
        img.save(favicon_path, sizes=config.FAVICON_SIZES, format="ICO")
        print("Favicon created")
    else:
        print("Favicon generation is disabled, skipping...")


def create_output_folder(path: str, force: bool = False, image_path: str = "") -> None:
    if not force and os.path.exists(path):
        input_text = f"The folder {path} already exists, you want to overwrite it? (y/n): "
        delete = input(input_text).lower() in ("y", "ye", "yes")
        if not delete:
            print("Exiting...")
            if os.path.exists(image_path):
                os.remove(image_path)
            exit(0)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    
    if force:
        print("Output folder overwritten")
    else:
        print("Output folder created")


def create_file(file_path: str, file_data: str) -> bool:
    # Create file directory
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    # Create file
    with open(file_path, "w+", encoding="utf-8") as file:
        file.write(file_data)


def create_files(image_path: str, output_path: str, categories: list) -> None:
    sizes = {}

    def create_files_recursive(dir: str, items: dict, depth: int):
        for k, v in items:
            if v:
                if is_file(k):
                    # File metadata
                    file_name = get_file_name(k)
                    file_path = os.path.join(dir, file_name)
                    image_dimensions = get_file_size(k, True)

                    # File data
                    if not sizes.get(image_dimensions) or is_rounded(k):
                        try:
                            print("Resizing", file_name, "to", image_dimensions)
                            img = Image.open(image_path)
                            img = square_image(img)
                            img = resize_image(img, image_dimensions)
                            if is_rounded(k):
                                img = round_image(img)
                            img.save(file_path)
                            sizes[image_dimensions] = file_path
                        except (ValueError, OSError):
                            print("Failed to create file", file_path)
                    else:
                        src_path = sizes.get(image_dimensions)
                        dst_path = file_path
                        shutil.copyfile(src_path, dst_path)
                        print("Copying file", file_name, "from", "/" + config.OUTPUT_FOLDER_NAME + src_path.replace(output_path, ""))
                elif depth != 1 or (depth == 1 and k in categories):
                    print("Creating directory", k)
                    folder_path = os.path.join(dir, k)
                    os.makedirs(folder_path)
                    if isinstance(v, dict):
                        create_files_recursive(folder_path, v.items(), depth + 1)

    create_files_recursive(output_path, config.SIZES.items(), 1)


def save_original_image(image_path: str, output_path: str) -> None:
    original_file_name = os.path.basename(image_path)
    original_file_name_ext = original_file_name.split(".")[1]
    file_name = "original." + original_file_name_ext 
    file_src = image_path
    file_dst = os.path.join(output_path, file_name)
    if os.path.exists(image_path):
        shutil.copyfile(file_src, file_dst)
        print("Original image saved")
    else:
        print("Failed to save original image")
    
def create_tmp_image(image_path: str, fetch_name: str) -> str:

    # Get file path
    original_image_path = os.path.abspath(image_path)
    if is_url(image_path):
        original_image_path = fetch_image(image_path, fetch_name)
    else:
        if not os.path.exists(original_image_path):
            print("Image does not exist")
            exit(0)

    # Copy to tmp file
    caller_path = os.getcwd()
    file_name = os.path.basename(original_image_path).split(".")[0]
    tmp_name = f"{file_name}-tmp.png"
    tmp_path = os.path.abspath(os.path.join(caller_path, tmp_name))

    # Resize image
    img = Image.open(original_image_path)
    w, h = img.size
    new_w = w
    new_h = h
    
    if w <= h and w >= config.MAX_IMAGE_SIZE:
        percentage = config.MAX_IMAGE_SIZE / w
        new_w = config.MAX_IMAGE_SIZE
        new_h = round(h * percentage)
    elif h >= config.MAX_IMAGE_SIZE:
        percentage = config.MAX_IMAGE_SIZE / h
        new_w = round(w * percentage)
        new_h = config.MAX_IMAGE_SIZE
    
    print(f"Resizing image from {w}x{h} to {new_w}x{new_h}")
    img = img.resize((new_w, new_h), Image.ANTIALIAS)
    img.save(tmp_path)

    if img.size[0] > config.WARN_IMAGE_SIZE or img.size[1] > config.WARN_IMAGE_SIZE:
        print("Image resizes, but is still very big. This might take some time...")
    else:
        print("Image resized")

    # Remove original image if fetched
    if is_url(image_path):
        os.remove(original_image_path)

    return tmp_path
