import os

# Files
FILE_TYPE = "png" # applies to all files except .ico files.
OUTPUT_FOLDER_NAME = "icons"

# Manifest
GENERATE_MANIFEST = True
GENERATE_FAVICON = True
FAVICON_SIZES = [(16, 16), (32, 32), (64, 64), (128, 128), (256, 256)]
MANIFEST_THEME_COLOR = "#ffffff"
MANIFEST_BACKGROUND_COLOR = "#ffffff"
MANIFEST_DISPLAY = "standalone" # standalone, browser, minimal-ui or fullscreen
MANIFEST_SCOPE = "/"
MANIFEST_START_URL = "/"
MANIFEST_NAME = "Name"
MANIFEST_SHORT_NAME = "Short name"

# Icon sizes
# HxW:name:attr1:attr2...

SIZES = {
    "web": {
        "16x16": True,
        "32x32": True,
        "64x64": True,
        "128x128": True,
        "256x256": True,
        "512x512": False,
        "1024x1024": False,
        "72x72:android-72": False,
        "96x96:android-96": False,
        "128x128:android-128": False,
        "144x144:android-144": False,
        "152x152:android-152": False,
        "192x192:android-192": False,
        "384x384:android-384": False,
        "512x512:android-512": False,
        "152x152:apple-touch-icon-ipad": True,
        "167x167:apple-touch-icon-ipad-retina": True,
        "180x180:apple-touch-icon-iphone-retina": True,
        "196x196:apple-touch-icon": True,
    }
}