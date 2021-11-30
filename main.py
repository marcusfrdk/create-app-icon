import argparse
from create import create_favicon, create_files, create_html_tags, create_manifest, create_output_folder
from utils import get_categories, get_image_path, get_output_path

def get_arguments():
    parser = argparse.ArgumentParser(usage="main.py path", description="Automate scaling and generation of icons, manifests and other data for web- or mobile apps.")
    parser.add_argument("path")
    parser.add_argument("-w", "--web", action="store_true")
    parser.add_argument("-a", "--android", action="store_true")
    parser.add_argument("-aw", "--apple-watch", action="store_true")
    parser.add_argument("-i", "--ios", action="store_true")
    parser.add_argument("-o", "--output")
    parser.add_argument("-f", "--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = get_arguments()
    image_path = get_image_path(args.path)
    output_path = get_output_path(image_path, args.output)
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
