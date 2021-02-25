import shutil, os
file_name = "sizes.py"
default_file_name = ".default.sizes.py"

if os.path.exists(file_name):
    os.remove(file_name)

if os.path.exists(default_file_name):
    shutil.copyfile(default_file_name, file_name)
    print("Successfully reset config.")
else:
    print("Could not reset config, please download it from the git repository.")