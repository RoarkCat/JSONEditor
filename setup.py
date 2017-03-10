import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ["xImage.png", "compareFileImage.png", "editFileImage.png", "newFileImage.png"]
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], "include_files": includefiles}


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "JSON_Editor",
        version = "0.1",
        description = "A GUI application for editing, creating, and comparing JSON!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("mainWindow.py", base=base)])