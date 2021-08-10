# Create App Icon

This script transforms an image to all the different sizes app icons. This script handles all XCode sizes and Android sizes for creating apps.

## Default Sizes

By default, the IOS icon sizes are set to the iPhones defaults. All Apple watch and Android sizes are checked.

## Installation

```bash
$ git clone https://github.com/marcusfrdk/create-app-icon
```

## How To Use

If you need more sizes than default, change what sizes you want in `sizes.py`, otherwise just run the following command.

```bash
python main.py PATH
```

## Flags

- [-f, --force] - Deletes output folder without confirmation

## Notes

To improve QoL, add this script to an alias and use it on any image wherever you are.
