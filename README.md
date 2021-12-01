<p align="center"><img src="https://i.imgur.com/RJLgSHK.png"/></p>

# Create App Icon

Automatically generate the required images for IOS-, Android-, Apple Watch- or web development in a single command.

## Requirements

- Python 3.7 or greater
- Numpy 1.19
- Pillow 8.3

## Installation

```bash
$ git clone https://github.com/marcusfrdk/create-app-icon
$ pip3 install -r requirements.txt
```

## Supported File Types

This script uses [Pillow](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) for image manipulation, meaning any image supported by the module is supported in this script.

## How To Use

Run the following command and replace 'path' with the local file path or a remote url.

```bash
python3 main.py path
```

## Example

### Normal

```bash
$ python3 main.py /images/dog.jpg
```

### Custom output folder name

```bash
$ python3 main.py /images/dog.jpg -o my-folder
```

### Only for specific device

```bash
$ python3 main.py /images/dog.jpg -i
```

\* _this creates icons only for IOS, see more flags below_

### Rounded favicon

This will round your favicon by 10 pixels. Change the number based on your favicon size.

```bash
$ python3 main.py /images/dog.jpg -fbr 10
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
| -fbr, --favicon-border-radius | Sets a border radius to the favicon, measured in pixels.    | No        |

\* _by default it creates everything_

## Alias (UNIX)

This script fully supports relative paths, in other words, this script can be used from anywhere on your computer. To call this script in an easy way, add a alias (UNIX-systems) to your .bashrc or .zprofile file.

```bash
...
alias cai='/path/to/main.py'
...
```

Then you can call the script from anywhere with:

```bash
$ cai image.png
```

## To do

- [ ] Add object recognition
- [ ] Add flag for only favicon
