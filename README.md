<p align="center"><img src="https://i.imgur.com/RQ9yeU9.png"/></p>

# Create App Icon

Automatically generate the required images for IOS-, Android-, Apple Watch- or web development in a single command.

## Requirements

- Python 3.7 or above

## Installation

```bash
$ git clone https://github.com/marcusfrdk/create-app-icon
$ pip3 install -r requirements.txt
```

## Supported File Types

This script uses [Pillow](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) for image manipulation, meaning any image supported by the module is supported in this script.

\* _remote files are only tested with png and jpg_

## How To Use

Run the following command and replace 'path' with the local file path or a remote url.

```bash
python3 main.py path
```

## Flags

| Flag                          | Description                                                 |  Required |
| ----------------------------- | ----------------------------------------------------------- | --------- |
| path                          | A file path or url                                          | Yes       |
| -f, --force                   |  Deletes the output folder without asking for confirmation. | No        |
| -o, --output                  |  Sets the output folder's name                              | No        |
| -w, --web                     |  Generates web image sizes, manifest, html tags and favicon | No        |
| -i, --ios                     |  Generates ios image sizes                                  | No        |
| -aw, --apple-watch            |  Generates Apple watch image sizes                          | No        |
| -a, --android                 |  Generates Android image sizes                              | No        |
| -fbr, --favicon-border-radius | Sets a border radius to the favicon                         | No        |

\* _by default it creates everything_

## UNIX Alias

This script fully supports relative paths, in other words, this script can be used from anywhere on your computer. To call this script in an easy way, add a alias (UNIX-systems) to your .bashrc or .zprofile file.

```bash
...
alias createAppIcon='/path/to/main.py'
...
```

Then you can call the script from anywhere with:

```bash
$ createAppIcon image.png
```

## To do

- [ ] Optimize the resizing process to speed up the script
- [ ] Use some sort of object recognition to center the "important" details in the image.
