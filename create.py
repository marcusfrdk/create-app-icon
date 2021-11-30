import shutil
import os
import config
import json
from parse import get_file_name, get_file_size, is_file, is_rounded
from PIL import Image
from transform import crop_image, resize_image, round_image

def create_manifest(output_path: str) -> None:
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
    else:
        print("Ignoring manifest...")


def create_favicon(output_path: str, image_path: str) -> None:
    if config.GENERATE_FAVICON:
        favicon_path = os.path.join(output_path, "web", "favicon.ico")
        img = Image.open(image_path)
        img = crop_image(img)
        img.save(favicon_path, sizes=config.FAVICON_SIZES)
        print("Favicon created")
    else:
        print("Favicon generation is disabled, skipping...")


def create_output_folder(path: str, ignore_confirmation: bool = False) -> None:
    if os.path.exists(path):
        if not ignore_confirmation:
            ans = input(f"The folder {path} already exists, do you want to remove it? (y/n) ").lower() in ["y", "ye", "yes"]
            if not ans:
                exit(0)
        shutil.rmtree(path)
    os.makedirs(path)


def create_file(file_path: str, file_data: str) -> bool:
    # Create file directory
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    # Create file
    with open(file_path, "w+", encoding="utf-8") as file:
        file.write(file_data)


def create_files(image_path: str, output_path: str, files: list[tuple]) -> None:
    for k, v in files:
        if is_file(k):
            # File metadata
            file_name = get_file_name(k)
            file_path = os.path.join(output_path, file_name)
            image_dimensions = get_file_size(k, True)

            print("Resizing", file_name, "to", image_dimensions)

            # File data
            try:
                img = Image.open(image_path)
                img = crop_image(img)
                img = resize_image(img, image_dimensions)
                if is_rounded(k):
                    img = round_image(img)
                img.save(file_path)
            except (ValueError, OSError):
                print("Failed to create file", file_path)
        else:
            print("Creating directory", k)
            folder_path = os.path.join(output_path, k)
            os.makedirs(folder_path)
            if isinstance(v, dict):
                create_files(image_path, folder_path, v.items())
