import argparse, os, shutil
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from sizes import sizes

parser = argparse.ArgumentParser(usage="main.py path", description="Automate the rounding, resizing and optimization of your newly created app icon.")
parser.add_argument("path")
parser.add_argument("-f", "--force", action="store_true")
args = parser.parse_args()

android_folder_name = "android_icons"
ios_folder_name = "ios_icons"
apple_watch_folder_name = "apple_watch_icons"

def get_image_name() -> str:
    if not args.path:
        return ""

    name = args.path.split("/")[-1].split(".")[0]
    return f"-{name}"

image_name = get_image_name()

caller_path = os.getcwd()
image_path = os.path.abspath(os.path.join(caller_path, args.path))
output_path = os.path.abspath(os.path.join(caller_path, f"output{image_name}"))
tmp_path = os.path.abspath(os.path.join(caller_path, "tmp.png"))

file_type = "png"

def crop_image(img: Image.Image) -> Image.Image:
    w, h = img.size

    s = min([w, h])

    left = (w - s)/2
    top = (h - s)/2
    right = (w + s)/2
    bottom = (h + s)/2

    return img.crop((left, top, right, bottom)).resize((1024, 1024), resample=Image.ANTIALIAS)

def squared(image: Image.Image, name: str, size: str): # Size is in format WxH
    height = int(size.split("x")[0])
    width = int(size.split("x")[1])

    resized = image.resize((height, width), Image.ANTIALIAS)
    resized.save(name, optimize=True, quality=90, format="PNG")


def rounded(image: Image.Image, name: str, size: str):
    # Resize image
    height = int(size.split("x")[0])
    width = int(size.split("x")[1])

    resized = image.resize((height, width), Image.ANTIALIAS).convert("RGB")

    # Round image
    npImage = np.array(resized)
    h, w = resized.size

    alpha = Image.new("L", resized.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage, npAlpha))
    Image.fromarray(npImage).save(name, optimize=True, quality=90, format="PNG")


def resize_android(image: Image.Image):
    # Reset path
    os.chdir(output_path)
    sizes_list = sizes["android"]

    android_folder = os.path.abspath(os.path.join(output_path, android_folder_name))
    
    icon_name = "ic_launcher." + file_type
    icon_name_round = "ic_launcher_round." + file_type

    # Create "android" folder
    if not os.path.exists(android_folder):
        os.makedirs(android_folder_name)
    os.chdir(android_folder)

    for k, v in sizes_list.items():
        size = k.split(":")[0]
        name = k.split(":")[1]

        if v:        
            # Create folder for images
            image_folder = os.path.abspath(os.path.join(android_folder, name))
            if os.path.exists(image_folder):
                shutil.rmtree(image_folder)
            os.makedirs(image_folder)
            os.chdir(image_folder)

            # Process images
            rounded(image, icon_name_round, size)
            squared(image, icon_name, size)

            os.chdir(caller_path)


def resize_apple(image: Image.Image, type:str, root: str):
    # Reset path
    os.chdir(output_path)
    root = os.path.abspath(os.path.join(output_path, root))

    # Create directory
    if not os.path.exists(root):
        os.makedirs(root)
    os.chdir(root)

    # Resize
    if sizes[type]:
        for size in sizes[type]:
            if sizes[type][size] == True:

                # Create image metadata
                height = int(size.split("x")[0])
                width = int(size.split("x")[1])
                name = str(height) + "." + file_type

                squared(image, name, size)


def clean():
    def confirm(name: str) -> bool:
        answer = input('The folder "%s" already exists. Do you want to delete it? (y/n): ' % name)
        if answer.lower() == "y" or answer.lower() == "ye" or answer.lower() == "yes":
            return True
        else:
            return False

    if os.path.exists(output_path):
        if args.force:
            shutil.rmtree(output_path)
        else:
            if confirm(output_path):
                shutil.rmtree(output_path)
            else:
                print("Exiting script...")
                exit()
    
    os.makedirs(output_path)

def finalize():
    folders = [
        android_folder_name,
        ios_folder_name,
        apple_watch_folder_name
    ]

    all_are_empty = True
    for name in folders:
        path = os.path.join(output_path, name)
        if len(os.listdir(path)) != 0:
            all_are_empty = False
        else:
            shutil.rmtree(path)

    if all_are_empty:
        shutil.rmtree(output_path)
        print("No sizes specified, please specify the sizes you want in 'sizes.py'")

    os.remove(tmp_path)

def convert(img: str) -> Image.Image:
    img = Image.open(img).save(tmp_path, format="PNG")
    img = Image.open(tmp_path).convert("RGBA")
    return img

if __name__ == "__main__":
    image = args.path

    if os.path.exists(image):
        # Clean
        clean()
        
        # Meta
        image = convert(image)
        # image = Image.open(image).convert("RGBA")
        
        # Run
        image = crop_image(image)
        resize_apple(image, "ios", ios_folder_name)
        resize_apple(image, "apple_watch", apple_watch_folder_name)
        resize_android(image)
        finalize()
    else:
        print("Image not valid, please select another one.")
        exit()