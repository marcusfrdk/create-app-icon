import argparse
from create import create_favicon, create_files, create_html_tags, create_manifest, create_output_folder, save_original_image
from fetch import fetch_image
from utils import clean, get_categories, get_output_path, is_url, get_image_path

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
    
    # Create output folder
    output_path = get_output_path(args.path, args.output)
    create_output_folder(output_path, args.force)

    image_path = get_image_path(args.path) if not is_url(args.path) else fetch_image(args.path, args.output)
    categories = get_categories(args)

    # Create images
    create_files(image_path, output_path, categories)

    # Create other files
    if "web" in categories:
        manifest = create_manifest(output_path)
        create_html_tags(output_path, manifest)
        create_favicon(output_path, image_path, args.favicon_border_radius)
    
    save_original_image(image_path, output_path)
    clean(image_path)


if __name__ == '__main__':
    main()
