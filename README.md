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

To run the program, run the following command:

```bash
$ python3 main.py source
```

_Use 'python' instead of 'python3' if you are on Windows_

## Flags

In order to customize and make the most of the program, there are some flags that can be used.

| Flag             | Description                                                      | Required preset | Type   |
| ---------------- | ---------------------------------------------------------------- | --------------- | ------ |
| source           | Path or uri to source image                                      | N/A             | string |
| -h, --help       | Shows help and available flags                                   | N/A             | bool   |
| -v, --verbose    | Shows more output messages                                       | N/A             | bool   |
| -f, --force      | Ignore confirmations                                             | N/A             | bool   |
| -o, --output     | Name of the output folder                                        | N/A             | string |
| --iphone         | Generate iPhone icons                                            | N/A             | bool   |
| --ipad           | Generate iPad icons                                              | N/A             | bool   |
| --apple-watch    | Generate Apple Watch icons                                       | N/A             | bool   |
| --web            | Generate web icons, favicon and manifest.json                    | N/A             | bool   |
| --android        | Generate Android icons                                           | N/A             | bool   |
| --align-top      | Aligns the image to the top                                      | N/A             | bool   |
| --align-bottom   | Aligns the image to the bottom                                   | N/A             | bool   |
| --align-offset   | Offset from the center, can be positive or negative              | N/A             | int    |
| --favicon-radius | Percentage value to round favicon, must be int between 0 and 100 | web             | int    |

_If no preset flags are provided, all presets will be generated._

## Credits

- [examples/landscape.jpg](https://unsplash.com/photos/HpVgq2BIjbw)
- [examples/portrait.jpg](https://unsplash.com/photos/odJtBMxGEfk)
