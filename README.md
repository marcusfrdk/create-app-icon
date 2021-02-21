# Create App Icon

Automate the rounding, resizing and optimization of your newly created app icon.

## Installation

Download this repo and run the scripts.

## Requirements

- Python 3

## How to use

1. Define what you need in the _config.py_ file.
2. Run `python3 main.py`.

## Config

### Rounded

Most Android phones need a rounded app icon due to Android themes. Set this option to true if you need rounded photos. _This will apply to all photos created_

### Optimized

The images will be minified and optimized when this option is set to **True**, thus the images will be processed, leading to image quality loss (Very little). Set this to **False** if you need the absolute best quality of your images.

### Sizes

Here you will select which sizes you need the app icon to be. If the size you need does not exist. Simply just add the `HxW` key with **True** or **False** as the value. If you need to reset the config back to its default state. Run the _reset.py_ script.
