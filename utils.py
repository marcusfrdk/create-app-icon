import shutil
import os

PRESETS = ["apple_watch", "android", "web", "iphone", "ipad"]

    
def confirm(prompt: str) -> bool:
    """ Require user confirmation """
    if args.force:
        print("Force is enabled, ignoring confirmation...")
    return input(prompt).lower() in ["y", "ye", "yes"] if not args.force else True


def verbose(*msg) -> None:
    """ Print to console if verbose mode is enabled """
    if args.verbose:
        print(*msg)


def should_run_all() -> bool:
    """ Check if any preset if enabled """
    for preset in PRESETS:
        if getattr(args, preset):
            return False
    return True


def initialize() -> str:
    # Get values
    global output_folder_path
    global output_folder_created

    name = args.source.split("/")[-1].split(".")[-2:-1][0]
    output_folder_path = os.path.join(os.getcwd(), "icons_" + name)
    output_folder_created = False
    all = should_run_all()
    
    if os.path.exists(output_folder_path):
        print(f"The folder {output_folder_path} already exists.")
        if confirm("Do you want to overwrite it? (y/n) "):         
            print(f"Removing {output_folder_path}...")
            shutil.rmtree(output_folder_path)
        else:
            exit(0)

    # Generate required files and dirs
    verbose(f"Creating folder '{output_folder_path}'...")
    os.makedirs(output_folder_path)
    for preset in PRESETS:
        folder_path = os.path.join(output_folder_path, preset)
        if (getattr(args, preset) or all) and not os.path.exists(folder_path):
            verbose(f"Creating folder '{folder_path}'...")
            os.makedirs(folder_path)
    output_folder_created = True


    return output_folder_path


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

    # Check if source path exists and is valid
    valid_image_types = ["png", "jpg", "jpeg"]
    if not os.path.exists(args.source):
        print(f"The file '{args.source}' does not exist")
        exit(1)
    elif args.source.split(".")[-1] not in valid_image_types:
        print("Image must be of type:", ", ".join(valid_image_types))
        exit(1)

    return args
