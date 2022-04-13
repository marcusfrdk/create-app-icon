def is_path(path: str) -> bool:
    """ Check if path is valid """
    from os.path import exists
    return exists(path)


def get_presets() -> dict:
    """ Get presets from presets.json """
    from json import load
    from os.path import dirname, join
    with open(join(dirname(__file__), 'presets.json')) as f:
        return load(f)

    
def confirm(prompt: str) -> bool:
    """ Require user confirmation """
    return input(prompt).lower() in ["y", "ye", "yes"]


def get_args() -> dict:
    """ Get arguments from command line """
    import argparse
    
    parser = argparse.ArgumentParser(description='Resize images to a given size.')
    parser.add_argument('source', type=str, help='path to source image')
    parser.add_argument("--iphone", help='generate iPhone icons', action="store_true")
    parser.add_argument("--ipad", help='generate iPad icons', action="store_true")
    parser.add_argument("--apple-watch", help='generate Apple Watch icons', action="store_true")
    parser.add_argument("--web", help='generate web icons', action="store_true")
    parser.add_argument("--android", help='generate Android icons', action="store_true")
    parser.add_argument("-v", "--verbose", help='show more output in terminal', action="store_true")
    args = parser.parse_args()

    # Check if any presets are given
    presets = get_presets()
    preset_names = [preset.replace("-", "_") for preset in presets.keys()]
    all = True
    for preset in preset_names:
        if getattr(args, preset):
            all = False
            break

    # Check if source path exists and is valid
    valid_image_types = ["png", "jpg", "jpeg"]
    if not is_path(args.source):
        print(f"The file '{args.source}' does not exist")
        exit(1)
    elif args.source.split(".")[-1] not in valid_image_types:
        print("Image must be of type:", ", ".join(valid_image_types))
        exit(1)

    return args, presets, all
