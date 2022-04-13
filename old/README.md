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
$ cd create-app-icon
$ pip3 install -r requirements.txt
```

## Supported File Types

This script uses [Pillow](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) for image manipulation, meaning any image supported by the module is supported in this script.

## How To Use

Run the following command and replace 'path' with the local file path or a remote url.

```bash
python3 main.py path
```

## Examples

### Normal

```bash
$ python3 main.py /images/dog.jpg
```

### Custom output folder name

```bash
$ python3 main.py /images/dog.jpg -o my-folder
```

### Only for a specific device

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
| -o, --output                  |  Sets the output folder name                                | No        |
| -w, --web                     |  Generates web images, manifest, html tags and favicon      | No        |
| -i, --ios                     |  Generates IOS images                                       | No        |
| -aw, --apple-watch            |  Generates Apple watch images                               | No        |
| -a, --android                 |  Generates Android images                                   | No        |
| -fbr, --favicon-border-radius | Sets a border radius to the favicon, measured in pixels.    | No        |

\* _by default, all device images are created_

## Alias

This script works relatively, so it can be used from anywhere in your terminal. A great way of makine this more accessible is by adding an alias, so you easily can call the script from anywhere.

### Add the alias to your .bashrc or .zprofile

```bash
...
alias cai='/path/to/create-app-icon/main.py'
...
```

\* 'cai' can be anything you want\_.

### Source the file

Once added to your source file, reload the terminal or refresh the terminal source by using one of the following commands.

#### Restart terminal

```bash
$ exec $SHELL
```

#### Refresh source

```bash
$ source ~/.bashrc
```

### Use it

Then you can call the file from anywhere with the following command.

```bash
$ cai image.png
```

## To do

- [ ] Add object recognition
- [ ] Add flag for only favicon
- [ ] Add loading animation when working