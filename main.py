import argparse, os, shutil
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from sizes import sizes


parser = argparse.ArgumentParser(usage="main.py path/to/source/image", description="Automate the rounding, resizing and optimization of your newly created app icon.")
parser.add_argument("src_path")
parser.add_argument("-r", "--rounded", action="store_true")
parser.add_argument("-i", "--ios", action="store_true")
parser.add_argument("-aw", "--apple-watch", action="store_true")
parser.add_argument("-a", "--android", action="store_true")
args = parser.parse_args()

caller_path = os.getcwd()
image_path = os.path.abspath(os.path.join(caller_path, args.src_path))

def squared(image, name, size): # Size is in format WxH
    height = int(size.split("x")[0])
    width = int(size.split("x")[1])

    resized = Image.open(image_path).resize((height, width))
    resized.save(name)

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
    Image.fromarray(npImage).save(name)

def resize_android(image):
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

    file_type = "." + str(args.src_path.split(".")[-1])

    android_folder_name = "android_icons"
    android_folder = os.path.abspath(os.path.join(caller_path, android_folder_name))
    
    icon_name = "ic_launcher" + file_type
    icon_name_round = "ic_launcher_round" + file_type

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

def resize2(type: str, image: str):
    sizes_type = sizes[type]
    file_type = image.split(".")[-1]

    os.chdir(os.path.abspath(os.path.join(caller_path, "out", type)))

    

    if sizes:
        for size in sizes_type:
            if sizes_type[size] == True:
                height = int(size.split("x")[0])
                width = int(size.split("x")[1])
                new_image = Image.open(os.path.abspath(os.path.join(caller_path, image)))
                out = new_image.resize((height, width))

                if args.rounded:
                    if android_name:
                        new_name = "ic_launcher_round" + "." + str(file_type)
                        rounded(out, name)
                    else:
                        new_name = str(size) + "_round" + "." + str(file_type)
                        rounded(out, new_name)

                else:
                    if android_name:
                        new_name = "ic_launcher." + str(file_type)
                        out.save(new_name, optimize=True)
                    else:
                        out.save(name, optimize=True)

                        

    os.chdir(caller_path)

                
                


def process(image):
    if args.ios:
        resize("ios", image)
    if args.apple_watch:
        resize("apple_watch", image)
    if args.android:
        resize_android(image)
    if not args.ios and not args.apple_watch and not args.android:
        print("Please select a device type.")
        exit()

if __name__ == "__main__":
    image = args.src_path

    shutil.rmtree("android_icons")

    if os.path.exists(image):
        image = Image.open(image).convert("RGB")
        w, h = image.size
        
        if w == h:
            print(args)
            process(image)
        else:
            print("The selected image must be square.")
            exit()
        
    else:
        print("Image not valid, please select another one.")
        exit()



# im = Image.open(args.src_path)
# new_size = (100, 100)
# out = im.resize(new_size)
# out.save("new-image.png")
# print("Done")