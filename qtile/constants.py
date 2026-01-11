import os

CONFIG_DIR = os.environ.get(
    "XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config")
)
ASSETS_DIR = os.path.join(CONFIG_DIR, "qtile", "assets")
