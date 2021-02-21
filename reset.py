import shutil, os

if os.path.exists("config.py"):
    os.remove("config.py")

if os.path.exists(".default.config.py"):
    shutil.copyfile(".default.config.py", "config.py")
    print("Successfully reset config.")
else:
    print("Could not reset config, please download it from the git repository.")