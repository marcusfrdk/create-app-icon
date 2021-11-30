import os
import argparse
from config import OUTPUT_FOLDER_NAME, SIZES
from create import create_favicon, create_files, create_manifest, create_output_folder

def get_arguments():
    parser = argparse.ArgumentParser(usage="main.py path", description="Automate the rounding, resizing and optimization of your newly created app icon.")
    parser.add_argument("path")
    parser.add_argument("-f", "--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = get_arguments()
    caller_path = os.getcwd()
    output_path = os.path.abspath(os.path.join(caller_path, OUTPUT_FOLDER_NAME))
    image_path = args.path

    # Create output folder
    create_output_folder(output_path, args.force)

    # Create images
    create_files(image_path, output_path, SIZES.items())

    # Create other files
    create_manifest(output_path)
    create_favicon(output_path, image_path)


if __name__ == '__main__':
    main()
