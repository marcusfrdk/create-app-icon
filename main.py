import utils


def initialize() -> None:
    # Get values
    name, ext = args.source.split("/")[-1].split(".")[-2:]
    print(name, ext)

    # Generate required directories


    print("Initializing...")


def generate_iphone() -> None:
    print("Generating iphone icons...")
    

def generate_android() -> None:
    print("Generating android icons...")


def generate_apple_watch() -> None:
    print("Generating apple watch icons...")


def generate_ipad() -> None:
    print("Generating ipad icons...")


def generate_web() -> None:
    print("Generating web icons...")


def main() -> None:
    global args
    args, all = utils.get_args()

    initialize()

    if args.iphone or all:
        generate_iphone()
    if args.ipad or all:
        generate_ipad()
    if args.android or all:
        generate_android()
    if args.apple_watch or all:
        generate_apple_watch()
    if args.web or all:
        generate_web()


if __name__ == "__main__":
    main()