![Banner](./assets/banner.png)

# Create App Icon

![top language](https://img.shields.io/github/languages/top/marcusfrdk/create-app-icon)
![code size](https://img.shields.io/github/languages/code-size/marcusfrdk/create-app-icon)
![last commit](https://img.shields.io/github/last-commit/marcusfrdk/create-app-icon)
![issues](https://img.shields.io/github/issues/marcusfrdk/create-app-icon)
![contributors](https://img.shields.io/github/contributors/marcusfrdk/create-app-icon)

Resize, scale and crop an image automatically to create all the required app icons for iOS, Android, Apple Watch and web development with a single command.

## Installation

To install the package, run the following commands:

```bash
$ git clone https://github.com/marcusfrdk/create-app-icon.git
$ cd create-app-icon
$ pip3 install -r requirements.txt
```

_Use 'pip' instead of 'pip3' if you are on Windows_

## Usage

To run the program, use the following command:

```bash
$ python3 main.py source
```

_Use 'python' instead of 'python3' if you are on Windows_

## Flags

| Flag             | Description                                         | Required Preset | Type   | Default |
| ---------------- | --------------------------------------------------- | --------------- | ------ | ------- |
| source           | Path or uri to source image                         |                 | string |         |
| -h, --help       | Shows help and available flags                      |                 | bool   |         |
| -v, --verbose    | Shows more output messages                          |                 | bool   |         |
| -f, --force      | Ignore confirmations                                |                 | bool   |         |
| -o, --output     | Name of the output folder                           |                 | string |         |
| --iphone         | Generate iPhone icons                               |                 | bool   |         |
| --ipad           | Generate iPad icons                                 |                 | bool   |         |
| --apple-watch    | Generate Apple Watch icons                          |                 | bool   |         |
| --web            | Generate web icons, favicon and manifest.json       |                 | bool   |         |
| --android        | Generate Android icons                              |                 | bool   |         |
| --offset         | Offset from the center, can be positive or negative |                 | int    |         |
| --top            | Aligns the image to the top                         |                 | bool   |         |
| --bottom         | Aligns the image to the bottom                      |                 | bool   |         |
| --favicon-radius | Percentage value to round favicon                   | web             | int    | 15      |
| --icon-radius    | Percentage value to round icons (icns, ico)         |                 | int    | 15      |
| --radius         | Percentage value to round all images                |                 | int    | 15      |

- If no preset flags are provided, all presets will be generated.
- Percentage values are between 0 and 100

## Alias

A recommendation is to add an alias to the main.py file. This will allow you to run the program without the need to specify the full path.

Add the following line in your .bashrc/.zshrc file:

```bash
...
alias ALIAS_NAME='/absolute/path/to/main.py'
...
```

## Credits

- [Landscape example image](https://unsplash.com/photos/HpVgq2BIjbw)
- [Portrait example image](https://unsplash.com/photos/odJtBMxGEfk)
