from config import FILE_TYPE

def get_file_name(file: str) -> str:
    name = file
    if ":" in file:
        name = file.split(":")[1]
    return f"{name}.{FILE_TYPE}"


def get_file_size(file: str, as_string: bool = False) -> str:
    if ":" in file:
        dim = file.split(":")[0]
        if as_string:
            return dim
        elif "x" in dim:
            dim = dim.split("x")[0]
            h = dim[0]
            w = dim[1]
            return (h, w)
        else:
            return file
    else:
        return file


def is_file(key: str) -> bool:
    if "x" in key:
        key = key.split("x")[0]
        return key.isnumeric()
    return False


def is_rounded(key: str) -> bool:
    return ":rounded" in key


def get_categories(args):
    categories = []
    if args.web:
        categories.append("web")
    if args.android:
        categories.append("android")
    if args.apple_watch:
        categories.append("apple_watch")
    if args.ios:
        categories.append("ios")

    if not args.ios and not args.web and not args.android and not args.apple_watch:
        categories = ["web", "ios", "apple_watch", "android"]
    
    return categories
