import os
import json

from debug import breakpoint

from AppKit import NSSearchPathForDirectoriesInDomains

APPNAME = "screenshot-processor"

file_dir = os.path.join(
    NSSearchPathForDirectoriesInDomains(14, 1, True)[0], APPNAME)
file_path = os.path.join(file_dir, "preferences.json")


def _initialize():
    if not os.path.isdir(file_dir):
        os.mkdir(file_dir)


def fetch_prefs():
    """Fetch prefererences for the app. 
    If no prefs exist, create a new prefs file and return the empty dict.

    Returns:
        dict: App preferences
    """
    try:
        with open(file_path, "r") as f:
            prefs = json.load(f)
            return prefs
    except FileNotFoundError:
        _initialize()
        prefs = {}
        with open(file_path, "w") as f:
            f.write("{}")
        return prefs


def write_pref(k, v):
    prefs = fetch_prefs()
    prefs[k] = v
    with open(file_path, "w") as f:
        prefs_json = json.dumps(prefs)
        f.write(prefs_json)
    return prefs