from setuptools import setup

APP = ["gui.py"]
DATA_FILES = ["icon.png"]
OPTIONS = {
    "argv_emulation": True,
    "includes": ["PyQt5.QtGui", "PyQt5.QtWidgets"],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
