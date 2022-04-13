from old.transform import crop_image
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
        name = f"{w}x{h}" if not name else name
        name = name + ".png"
        dst = os.path.join(root_path, name)
        src = tmp_sq_path

        if w != h:
            src = tmp_org_path
            utils.scale_image(src, dst, max(w, h))
            utils.crop_image(dst, dst, w, h)
        else:
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
        if args.iphone or all: # iPhone
            sizes = presets["iphone"]
            generate_images(sizes, "iphone")
        if args.ipad or all: # iPad
            sizes = presets["ipad"]
            generate_images(sizes, "ipad")
        if args.android or all: # Android
            sizes = presets["android"]
            for size in sizes:
                size, folder_name = size.split(":")
                folder_path = os.path.join(output_folder_path, "android", folder_name)
                os.makedirs(folder_path, exist_ok=True)
                w, h = utils.get_dimensions(size)
                sq_path = os.path.join(folder_path, "ic_launcher.png")
                rn_path = os.path.join(folder_path, "ic_launcher_round.png")
                utils.resize_image(tmp_sq_path, sq_path, w, h)
                if folder_name != "play_store":
                    utils.round_image(sq_path, rn_path)
        if args.apple_watch or all: # Apple Watch
            sizes = presets["apple_watch"]
            generate_images(sizes, "apple_watch")
        if args.web or all: # Web
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
