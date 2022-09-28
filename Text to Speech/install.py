from sys import platform
from pathlib import Path
import importlib
import bpy

from .installers import osx
from .installers import linux
from .installers import windows
from .installers import other
importlib.reload(osx)
importlib.reload(linux)
importlib.reload(windows)
importlib.reload(other)

def install(module):

    print(f"attempting {module} install on {platform} blender version {bpy.app.version}")

    if platform.startswith("linux"):
        return linux.install(module)
    elif platform == "win32":
        return windows.install(module)
    elif platform == "darwin":
        return osx.install(module)
    else:
        return other.install(module)