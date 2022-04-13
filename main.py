import utils
import os
import shutil


def initialize() -> None:
    # Get values
    name, ext = args.source.split("/")[-1].split(".")[-2:]
    output_folder_path = os.path.join(os.getcwd(), "icons-" + name)
    if os.path.exists(output_folder_path):
        print(f"The folder {output_folder_path} already exists.")
        if utils.confirm("Do you want to overwrite it? (y/n) "):
            print(f"Removing {output_folder_path}...")
            shutil.rmtree(output_folder_path)
        else:
            exit(0)

    # Generate required files and dirs
    os.makedirs(output_folder_path)


    print("Initializing...")


def clean():
    print("Aborting...")


def generate_iphone() -> None:
    print("Generating iphone icons...")
    

def generate_android() -> None:
    print("Generating android icons...")


def generate_apple_watch() -> None:
    print("Generating apple watch icons...")


def generate_ipad() -> None:
    print("Generating ipad icons...")


def generate_web() -> None:
    print("Generating web icons...")


def main() -> None:
    global args
    args, all = utils.get_args()

    try:
        initialize()

        if args.iphone or all:
            generate_iphone()
        if args.ipad or all:
            generate_ipad()
        if args.android or all:
            generate_android()
        if args.apple_watch or all:
            generate_apple_watch()
        if args.web or all:
            generate_web()
    except:
        clean()

if __name__ == "__main__":
    main()