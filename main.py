import os
import argparse
from config import OUTPUT_FOLDER_NAME
from create import create_favicon, create_files, create_html_tags, create_manifest, create_output_folder
from parse import get_categories

def get_arguments():
    parser = argparse.ArgumentParser(usage="main.py path", description="Automate the rounding, resizing and optimization of your newly created app icon.")
    parser.add_argument("path")
    parser.add_argument("-w", "--web", action="store_true")
    parser.add_argument("-a", "--android", action="store_true")
    parser.add_argument("-aw", "--apple-watch", action="store_true")
    parser.add_argument("-i", "--ios", action="store_true")
    parser.add_argument("-f", "--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = get_arguments()
    caller_path = os.getcwd()
    output_path = os.path.abspath(os.path.join(caller_path, OUTPUT_FOLDER_NAME))
    image_path = args.path
    categories = get_categories(args)

    # Create output folder
    create_output_folder(output_path, args.force)

    # Create images
    create_files(image_path, output_path, categories)

    # Create other files
    if "web" in categories:
        manifest = create_manifest(output_path)
        create_html_tags(output_path, manifest)
        create_favicon(output_path, image_path)


if __name__ == '__main__':
    main()
