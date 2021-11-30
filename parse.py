from config import FILE_TYPE

def get_file_name(file: str) -> str:
    if ":" in file:
        name = file.split(":")[1]
        return f"{name}.{FILE_TYPE}"
    else:
        return file

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