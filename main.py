import argparse, os, shutil
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from sizes import sizes


parser = argparse.ArgumentParser(usage="main.py path/to/source/image", description="Automate the rounding, resizing and optimization of your newly created app icon.")
parser.add_argument("src_path")
parser.add_argument("-f", "--force", action="store_true")
parser.add_argument("-r", "--rounded", action="store_true")
parser.add_argument("-i", "--ios", action="store_true")
parser.add_argument("-aw", "--apple-watch", action="store_true")
parser.add_argument("-a", "--android", action="store_true")
args = parser.parse_args()

android_folder_name = "android_icons"
ios_folder_name = "ios_icons"
apple_watch_folder_name = "apple_watch_icons"

caller_path = os.getcwd()
image_path = os.path.abspath(os.path.join(caller_path, args.src_path))

file_type = str(args.src_path.split(".")[-1])


def squared(image, name, size): # Size is in format WxH
    height = int(size.split("x")[0])
    width = int(size.split("x")[1])

    resized = Image.open(image_path).resize((height, width))
    resized.save(name, optimize=True, quality=90)


def rounded(image, name, size):
    # Resize image
    height = int(size.split("x")[0])
    width = int(size.split("x")[1])

    resized = Image.open(image_path).resize((height, width))
    
    # Round image
    npImage = np.array(resized)
    h, w = resized.size

    alpha = Image.new("L", resized.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage, npAlpha))
    Image.fromarray(npImage).save(name, optimize=True, quality=90)


def resize_android(image):
    # Reset path
    os.chdir(caller_path)

    # List of names
    android_names = {
        "36x36": "mipmap-ldpi",             # LDPI
        "48x48": "mipmap-mdpi",             # MDPI
        "72x72": "mipmap-hdpi",             # HDPI
        "96x96": "mipmap-xhdpi",            # XHDPI
        "144x144": "mipmap-xxhdpi",         # XXHDPI
        "192x192": "mipmap-xxxhdpi",        # XXXHDPI
        "512x512": "play-store"             # GOOGLE PLAY STORE
    }

    sizes_list = sizes["android"]

    android_folder = os.path.abspath(os.path.join(caller_path, android_folder_name))
    
    icon_name = "ic_launcher." + file_type
    icon_name_round = "ic_launcher_round." + file_type

    for size in sizes_list:
        if sizes_list[size] == True:
            # Create "android" folder
            if not os.path.exists(android_folder):
                os.makedirs(android_folder_name)
            os.chdir(android_folder)
            
            # Create folder for images
            image_folder = os.path.abspath(os.path.join(android_folder, android_names[size]))
            os.makedirs(image_folder)
            os.chdir(image_folder)

            # Process images
            rounded(image, icon_name_round, size)
            squared(image, icon_name, size)

            os.chdir(caller_path)


def resize_other(image, type:str, root: str):
    # Reset path
    os.chdir(caller_path)
    root = os.path.abspath(os.path.join(caller_path, root))

    # Resize
    if sizes[type]:
        for size in sizes[type]:
            if sizes[type][size] == True:
                # Create directory
                if not os.path.exists(root):
                    os.makedirs(root)
                os.chdir(root)

                # Create image metadata
                height = int(size.split("x")[0])
                width = int(size.split("x")[1])
                name = str(size) + "." + file_type

                if(args.rounded):
                    rounded(image, name, size)
                else:
                    squared(image, name, size)


def process(image):
    if args.ios:
        resize_other(image, "ios", ios_folder_name)
    if args.apple_watch:
        resize_other(image, "apple_watch", apple_watch_folder_name)
    if args.android:
        resize_android(image)
    if not args.ios and not args.apple_watch and not args.android:
        print("Please select a device type.")
        exit()


def clean():
    def confirm(name: str) -> bool:
        answer = input('The folder "%s" already exists. Do you want to delete it? (y/n): ' % name)
        if answer.lower() == "y" or answer.lower() == "ye" or answer.lower() == "yes":
            return True
        else:
            return False


    def delete(name: str):
        if os.path.exists(os.path.join(caller_path, name)):
            if args.force:
                shutil.rmtree(name)
            else:
                if confirm(name):
                    shutil.rmtree(name)
                else:
                    print("Exiting script...")
                    exit()


    if args.android:
        delete(android_folder_name)
    
    if args.ios:
        delete(ios_folder_name)

    if args.apple_watch:
        delete(apple_watch_folder_name)


if __name__ == "__main__":
    image = args.src_path

    if os.path.exists(image):
        # Clean
        clean()
        
        # Meta
        image = Image.open(image).convert("RGB")
        h, w = image.size
        
        # Run
        if w == h:
            process(image)
        else:
            print("The selected image must be square.")
            exit()
        
    else:
        print("Image not valid, please select another one.")
        exit()