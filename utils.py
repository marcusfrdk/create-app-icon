import shutil
import os

    
def confirm(prompt: str) -> bool:
    """ Require user confirmation """
    return input(prompt).lower() in ["y", "ye", "yes"] if not args.force else True


def verbose(*msg) -> None:
    """ Print to console if verbose mode is enabled """
    if args.verbose:
        print(*msg)


def initialize() -> None:
    # Get values
    global output_folder_path
    global output_folder_created
    name = args.source.split("/")[-1].split(".")[-2:-1][0]
    output_folder_path = os.path.join(os.getcwd(), "icons-" + name)
    output_folder_created = False
    if os.path.exists(output_folder_path):
        print(f"The folder {output_folder_path} already exists.")
        if confirm("Do you want to overwrite it? (y/n) "):
            print(f"Removing {output_folder_path}...")
            shutil.rmtree(output_folder_path)
        else:
            exit(0)

    # Generate required files and dirs
    os.makedirs(output_folder_path)
    output_folder_created = True

    print("Initializing...")


def clean():
    print("Aborting...")
    if output_folder_created:
        verbose(f"Removing {output_folder_path}...")
        shutil.rmtree(output_folder_path)


def get_args() -> dict:
    """ Get arguments from command line """
    import argparse

    global args
    
    parser = argparse.ArgumentParser(description='Resize images to a given size.')
    parser.add_argument('source', type=str, help='path to source image')
    parser.add_argument("--iphone", help='generate iPhone icons', action="store_true")
    parser.add_argument("--ipad", help='generate iPad icons', action="store_true")
    parser.add_argument("--apple-watch", help='generate Apple Watch icons', action="store_true")
    parser.add_argument("--web", help='generate web icons', action="store_true")
    parser.add_argument("--android", help='generate Android icons', action="store_true")
    parser.add_argument("-v", "--verbose", help='show more output in terminal', action="store_true")
    parser.add_argument("-f", "--force", help='ignores any confirmations', action="store_true")
    args = parser.parse_args()

    # Check if any presets are given
    all = True
    presets = ["apple_watch", "android", "web", "iphone", "ipad"]
    for preset in presets:
        if getattr(args, preset):
            all = False
            break

    # Check if source path exists and is valid
    valid_image_types = ["png", "jpg", "jpeg"]
    if not os.path.exists(args.source):
        print(f"The file '{args.source}' does not exist")
        exit(1)
    elif args.source.split(".")[-1] not in valid_image_types:
        print("Image must be of type:", ", ".join(valid_image_types))
        exit(1)

    return args, all
