# Create App Icon

This script will take any squared image and transform it to a valid mobile app icon by just checking the needed sizes in `sizes.py`. 

## Installation

### Clone

```bash
$ git clone https://github.com/marcusfrdk/create-app-icon.git
```

### Download

Download the repository using the download button.

## How to use
1. Configure sizes.py
2. Run main script
```bash
$ python3 main.py [path] [flags]
```
3. Reset sizes (optional)
```bash
$ python3 reset.py
```

## Flags

### Required
- [PATH] - Path to image (absolute or relative)

### Optional
- [-i, --ios] - Create IOS app icon(s)
- [-aw, --apple-watch] - Create Apple Watch icon(s)
- [-a, --android] - Create Android icon(s)
- [-f, --force] - Force delete output folders
- [-r, --rounded] - Create circular icons

## Notes
- Images need to be squared (height is equal to width)
- Path can be absolute or relative
- Output folder names can be configured in the main.py script.
