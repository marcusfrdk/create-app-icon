import utils
import os
import shutil
import traceback


def initialize() -> None:
    # Get values
    global output_folder_path
    global output_folder_created
    name = args.source.split("/")[-1].split(".")[-2:-1][0]
    output_folder_path = os.path.join(os.getcwd(), "icons-" + name)
    output_folder_created = False
    if os.path.exists(output_folder_path):
        print(f"The folder {output_folder_path} already exists.")
        if utils.confirm("Do you want to overwrite it? (y/n) "):
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
        if args.verbose:
            print(f"Removing {output_folder_path}...")
        shutil.rmtree(output_folder_path)


def generate_iphone(sizes: list) -> None:
    print("Generating iphone icons...")
    

def generate_android(sizes: list) -> None:
    print("Generating android icons...")


def generate_apple_watch(sizes: list) -> None:
    print("Generating apple watch icons...")


def generate_ipad(sizes: list) -> None:
    print("Generating ipad icons...")


def generate_web(sizes: list) -> None:
    print("Generating web icons...")


def main() -> None:
    global args
    args, presets, all = utils.get_args()

    try:
        initialize()

        if args.iphone or all:
            generate_iphone(presets["iphone"])
        if args.ipad or all:
            generate_ipad(presets.ipad)
        if args.android or all:
            generate_android(presets.android)
        if args.apple_watch or all:
            generate_apple_watch(presets.apple_watch)
        if args.web or all:
            generate_web(presets.web)
    except:
        if args.verbose:
            traceback.print_exc()
        clean()


if __name__ == "__main__":
    main()
