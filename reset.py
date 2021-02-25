import shutil, os

# Meta
file_name = "sizes.py"
file_path = os.path.abspath(os.path.join(__file__, "..", file_name))

default_file_name = ".default.sizes.py"
default_file_path = os.path.abspath(os.path.join(__file__, "..", default_file_name))

# Current config file
if os.path.exists(file_path):
    os.remove(file_path)

# Default config file
if os.path.exists(default_file_path):
    shutil.copyfile(default_file_path, file_path)
    print("Successfully reset config.")
else:
    print("Could not reset config, please download it from the git repository.")