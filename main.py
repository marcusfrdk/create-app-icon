import argparse, os, shutil
from PIL import Image
from config import config

caller_path = os.getcwd()

parser = argparse.ArgumentParser(usage="main.py path/to/source/image", description="Automate the rounding, resizing and optimization of your newly created app icon.")
parser.add_argument("src_path")
args = parser.parse_args()

def optimize():
    print("Optimizing image...")

def rounded() -> bool:
    print("Rounding image...")

def resize(type: str, image: str):
    sizes = config["sizes"]
    sizes_type = sizes[type]
    file_type = image.split(".")[-1]

    os.chdir(os.path.abspath(os.path.join(caller_path, "out", type)))

    if sizes:
        for size in sizes_type:
            if sizes_type[size] == True:
                height = int(size.split("x")[0])
                width = int(size.split("x")[1])
                new_image = Image.open(os.path.abspath(os.path.join(caller_path, image)))
                new_name = str(size) + "." + str(file_type)
                out = new_image.resize((height, width))
                out.save(new_name)

    os.chdir(caller_path)

                
                


def process(image):
    rounded = config["rounded"]
    optimized = config["optimized"]

    resize("ios", image)
    resize("apple-watch", image)
    resize("android", image)

def clean():
    if os.path.exists("out"):
        answer = input("There seems to be an existing output folder, would you like to delete it? (y/n): ")
        if answer.lower() == "y":
            shutil.rmtree("out")
        else:
            print("Exiting script")
            exit()

def create_output():
    os.makedirs("out")
    os.chdir("out")
    os.makedirs("ios")
    os.makedirs("android")
    os.makedirs("apple-watch")
    os.chdir("..")

if __name__ == "__main__":
    image = args.src_path

    if os.path.exists(image):
        dimensions = Image.open(image)
        is_valid = dimensions.size[0] == dimensions.size[1]


        if is_valid:
            #clean()
            #create_output()
            process(image)
        else:
            print("The selected image must be square.")
            exit()
        
    else:
        print("Source path is not valid, please specify another one.")
        exit()



# im = Image.open(args.src_path)
# new_size = (100, 100)
# out = im.resize(new_size)
# out.save("new-image.png")
# print("Done")