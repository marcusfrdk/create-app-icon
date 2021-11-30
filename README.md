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

## How To Use

Run the following command and replace 'path' with the path to your image (or simply file name).

```bash
python3 main.py path
```

## Flags

| Flag                          | Description                                                 |  Required |
| ----------------------------- | ----------------------------------------------------------- | --------- |
| path                          | The path to your image                                      | Yes       |
| -f, --force                   |  Deletes the output folder without asking for confirmation. | No        |
| -o, --output                  |  Sets the output folder's name                              | No        |
| -w, --web                     |  Generates web image sizes, manifest, html tags and favicon | No        |
| -i, --ios                     |  Generates ios image sizes                                  | No        |
| -aw, --apple-watch            |  Generates Apple watch image sizes                          | No        |
| -a, --android                 |  Generates Android image sizes                              | No        |
| -fbr, --favicon-border-radius | Sets a border radius to the favicon                         | No        |

\* _by default the script creates icons for ios, apple watch, android and web_

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

- [ ] Add support for remote image fetching
- [ ] Optimize the resizing process to speed up the script
- [ ] Use some sort of object recognition to center the "important" details in the image.
