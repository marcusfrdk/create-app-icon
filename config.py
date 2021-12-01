# Files
FILE_TYPE = "png" # applies to all files except .ico files.
OUTPUT_FOLDER_NAME = "icons"
MAX_IMAGE_SIZE = 1024

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
    "ios": {
        "16x16": False,
        "20x20": False,
        "24x24": False,
        "29x29": False,
        "32x32": False,
        "40x40": True,
        "48x48": False,
        "50x50": False,
        "57x57": False,
        "58x58": True,
        "60x60": True,
        "64x64": False,
        "72x72": False,
        "76x76": False,
        "80x80": True,
        "87x87": True,
        "100x100": False,
        "114x114": False,
        "120x120": True,
        "128x128": False,
        "167x167": False,
        "144x144": False,
        "152x152": False,
        "180x180": True,
        "256x256": False,
        "512x512": False,
        "1024x1024": True
    },
    "apple_watch": {
        "48x48": True,
        "55x55": True,
        "58x58": True,
        "80x80": True,
        "87x87": True,
        "88x88": True,
        "100x100": True,
        "172x172": True,
        "196x196": True,
        "216x216": True,
        "1024x1024": True,
    },
    "android": {
        "mipmap-ldpi": {
            "36x36:ic_launcher": True,
            "36x36:ic_launcher_round:rounded": True,
        },
        "mipmap-mdpi": {
            "48x48:ic_launcher": True,
            "48x48:ic_launcher_round:rounded": True,
        },
        "mipmap-hdpi": {
            "72x72:ic_launcher": True,
            "72x72:ic_launcher_round:rounded": True,
        },
        "mipmap-xhdpi": {
            "96x96:ic_launcher": True,
            "96x96:ic_launcher_round:rounded": True,
        },
        "mipmap-xxhdpi": {
            "144x144:ic_launcher": True,
            "144x144:ic_launcher_round:rounded": True,
        },
        "mipmap-xxxhdpi": {
            "192x192:ic_launcher": True,
            "192x192:ic_launcher_round:rounded": True,
        },
        "play_store": {
            "512x512": True
        }
    },
    "web": {
        "16x16": True,
        "32x32": True,
        "64x64": True,
        "128x128": True,
        "256x256": True,
        "512x512": True,
        "1024x1024": True,
        "72x72:android-72": True,
        "96x96:android-96": True,
        "128x128:android-128": True,
        "144x144:android-144": True,
        "152x152:android-152": True,
        "192x192:android-192": True,
        "384x384:android-384": True,
        "512x512:android-512": True,
        "152x152:apple-touch-icon-ipad": True,
        "167x167:apple-touch-icon-ipad-retina": True,
        "180x180:apple-touch-icon-iphone-retina": True,
        "196x196:apple-touch-icon": True,
        "196x196:apple-touch-startup-image": True,
    }
}