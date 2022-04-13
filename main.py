import utils
import traceback
import os
import json


def generate_tmp_images() -> str:
    global tmp_sq_path
    global tmp_org_path

    tmp_sq_path = os.path.join(output_folder_path, "tmp-sq.png")
    tmp_org_path = os.path.join(output_folder_path, "tmp-org.png")

    utils.scale_image(args.source, tmp_org_path, 1024)
    utils.crop_image(tmp_org_path, tmp_sq_path)


def generate_images(sizes: list, root_folder: str) -> None:
    root_path = os.path.join(output_folder_path, root_folder)
    for size in sizes:
        name = None
        if ":" in size:
            size, name = size.split(":")
        w, h = utils.get_dimensions(size)
        src = tmp_sq_path if w == h else tmp_org_path
        name = f"{w}x{h}" if not name else name
        name = name + ".png"
        dst = os.path.join(root_path, name)
        utils.verbose(f"Generating '{name}' in folder '{root_folder}'...")
        utils.resize_image(src, dst, w, h)


def main() -> None:
    global args
    global output_folder_path
    global presets

    args = utils.get_args()
    all = utils.should_run_all()
    presets = json.load(open("presets.json", "r"))

    try:
        output_folder_path = utils.initialize()
        generate_tmp_images()
        if args.iphone or all:
            sizes = presets["iphone"]
            generate_images(sizes, "iphone")
        if args.ipad or all:
            sizes = presets["ipad"]
            generate_images(sizes, "ipad")
        if args.android or all:
            pass
        if args.apple_watch or all:
            sizes = presets["apple_watch"]
            generate_images(sizes, "apple_watch")
        if args.web or all:
            sizes = presets["web"]
            generate_images(sizes, "web")
    except:
        if args.verbose:
            traceback.print_exc()
            utils.clean()
            exit(1)
    utils.clean(True)


if __name__ == "__main__":
    main()
