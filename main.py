import utils
import traceback
import functions


def main() -> None:
    global args
    args, all = utils.get_args()

    try:
        utils.initialize()
        if args.iphone or all:
            functions.preset_iphone()
        if args.ipad or all:
            functions.preset_ipad()
        if args.android or all:
            functions.preset_android()
        if args.apple_watch or all:
            functions.preset_apple_watch()
        if args.web or all:
            functions.preset_web()
    except:
        if args.verbose:
            traceback.print_exc()
        utils.clean()


if __name__ == "__main__":
    main()
