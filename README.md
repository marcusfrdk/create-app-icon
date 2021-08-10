<p align="center"><img src="https://i.imgur.com/RQ9yeU9.png"/></p>

# Create App Icon

Transform an image to all the required app icon sizes at once.

## Default Sizes

By default, the IOS icon sizes are set to the iPhone's defaults. All Apple watch and Android sizes are checked.

## Installation

```bash
$ git clone https://github.com/marcusfrdk/create-app-icon
```

## Supported File Types

Since this script uses PILLOW for image handling, the script supports the same file types as it does.

[Supported file types](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)

## How To Use

This script is very unopinionated when it comes to file type or call location. _You can run this script from anywhere in your filesystem._

```bash
python main.py PATH
```

_Change the output sizes in `sizes.py`_

## Flags

- [-f, --force] - Deletes output folder without confirmation

## Notes

To improve QoL, add this script to an alias and use it on any image wherever you are in your file system.

### .bashrc

```bash
...
alias alias_name = 'python /path/to/script/main.py'
...
```

_This will allow you to use the script anywhere by running the set command name_
