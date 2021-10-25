import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import screenshot
import app_data

from debug import breakpoint, popup

app = QApplication([])
app.setQuitOnLastWindowClosed(False)


def reconfigure_save_directory():
    dirname = str(QFileDialog.getExistingDirectory(None, "Select Folder"))
    if not dirname:
        popup("You need to select a directory to save your PDF.")
        return app_data.fetch_prefs()
    return app_data.write_pref("file_location", dirname)


# Load the app preferences
prefs = app_data.fetch_prefs()
if "file_location" not in prefs:
    popup("Please select a folder to save your PDF.")
    prefs = reconfigure_save_directory()

    # File location STILL wasn't written, we should quit
    if "file_location" not in prefs:
        import sys
        sys.exit(0)

ssp = screenshot.ScreenshotProcessing()
ssp.path = prefs["file_location"]

# Adding an icon
icon_path = os.path.join(os.getcwd(), "icon.png")
icon = QIcon(icon_path)

# Adding item on the menu bar
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)


# Callback functions to be called when triggered by the menu items
def start_rec_func():
    try:
        ssp.start_recording_screen()
        popup("Started recording!")
    except screenshot.ScreenshotProcessingException as e:
        popup(str(e))


def stop_rec_func():
    try:
        ssp.stop_recording_screen()
        popup("Stopped recording")
    except screenshot.ScreenshotProcessingException as e:
        popup(str(e))


def reconfigure_dir_func():
    prefs = reconfigure_save_directory()
    reconfigure.setText(f"Saving to: {prefs['file_location']}")
    ssp.path = prefs["file_location"]


def quit_func():
    if ssp.rt is not None:
        ssp.stop_recording_screen()
    app.quit()


# Creating the options
menu = QMenu()

# Start recording the screen
start_rec = QAction("Start Recording")
start_rec.triggered.connect(start_rec_func)
menu.addAction(start_rec)

# Stop recording the screen
stop_rec = QAction("Stop Recording")
stop_rec.triggered.connect(stop_rec_func)
menu.addAction(stop_rec)

# Reconfigure the save directory
reconfigure = QAction(f"Saving to: {prefs['file_location']}")
reconfigure.triggered.connect(reconfigure_dir_func)
menu.addAction(reconfigure)

# Quit the app
quit = QAction("Quit")
quit.triggered.connect(quit_func)
menu.addAction(quit)

# Adding options to the System Tray
tray.setContextMenu(menu)

app.exec()
