import utils
import traceback
import os


def generate_image(src: str, dst: str, size: str) -> None:
    h, w = size.split("x")


def preset_iphone() -> None:    
    print("Generating iphone icons...")
    

def preset_android() -> None:
    print("Generating android icons...")


def preset_apple_watch() -> None:
    print("Generating apple watch icons...")


def preset_ipad() -> None:
    print("Generating ipad icons...")


def preset_web() -> None:
    print("Generating web icons...")


def main() -> None:
    global args
    global output_folder_path

    args = utils.get_args()
    all = utils.should_run_all()

    try:
        output_folder_path = utils.initialize()
        if args.iphone or all:
            preset_iphone()
        if args.ipad or all:
            preset_ipad()
        if args.android or all:
            preset_android()
        if args.apple_watch or all:
            preset_apple_watch()
        if args.web or all:
            preset_web()
    except:
        if args.verbose:
            traceback.print_exc()
        utils.clean()


if __name__ == "__main__":
    main()
