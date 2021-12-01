import argparse
from create import create_favicon, create_files, create_html_tags, create_manifest, create_output_folder, create_tmp_image, save_original_image
from utils import clean, get_categories, get_fetch_name, get_output_folder_path

def get_arguments():
    parser = argparse.ArgumentParser(usage="main.py path", description="Automate scaling and generation of icons, manifests and other data for web- or mobile apps.")
    parser.add_argument("path")
    parser.add_argument("-w", "--web", action="store_true")
    parser.add_argument("-a", "--android", action="store_true")
    parser.add_argument("-aw", "--apple-watch", action="store_true")
    parser.add_argument("-i", "--ios", action="store_true")
    parser.add_argument("-o", "--output")
    parser.add_argument("-fbr", "--favicon-border-radius")
    parser.add_argument("-f", "--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = get_arguments()

    # Metadata
    fetch_name = get_fetch_name()
    image_path = create_tmp_image(args.path, fetch_name)
    # output_folder_path = get_output_folder_path(image_path, args.output, fetch_name)
    # categories = get_categories(args)

    # create_output_folder(output_folder_path, args.force)

    # # Create files
    # create_files(image_path, output_folder_path, categories)

    # # Create other files
    # if "web" in categories:
    #     manifest = create_manifest(output_folder_path)
    #     create_html_tags(output_folder_path, manifest)
    #     create_favicon(output_folder_path, image_path, args.favicon_border_radius)
    # save_original_image(image_path, output_folder_path)

    # # Clean
    # clean(image_path, args)

if __name__ == '__main__':
    main()

    # IMprove performance
    # Resize original image to max height of 1024