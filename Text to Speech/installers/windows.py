import subprocess
from pathlib import Path
import os
import sys
import bpy
import importlib

def install_module(module, test):
    if bpy.app.version < (2, 92, 0):
        subprocess.call([str(py_exec), "-m", "ensurepip", "--user"])
        subprocess.call([str(py_exec), "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.call([str(py_exec),"-m", "pip", "install", "--user", module])
    else:
        py_exec = str(sys.executable)
        lib = os.path.join(Path(py_exec).parent.parent, "lib")
        subprocess.call([py_exec, "-m", "ensurepip", "--user" ])
        subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "pip" ])
        subprocess.call([py_exec,"-m", "pip", "install", f"--target={str(lib)}", module])
    try:
        importlib.import_module(test)
        return(True)
    except:
        return(False)


def install(module):
    return install_module(module, module)

def pypiwin32_append_paths():
    py_exec = str(sys.executable)
    base = Path(py_exec).parent.parent
    lib = os.path.join(base, "lib", "win32", "lib")
    sys.path.append(lib)
    lib = os.path.join(base, "lib", "win32")
    sys.path.append(lib)
    file1 = os.path.join(base, "lib", "pywin32_system32", "pythoncom310.dll")
    file2 = os.path.join(base, "lib", "pywin32_system32", "pywintypes310.dll")
    target1 = os.path.join(base, "lib", "win32", "lib", "pythoncom310.dll")
    target2 = os.path.join(base, "lib", "win32", "lib", "pywintypes310.dll")

    if not os.path.exists(target1):
        Path(file1).rename(target1)
        Path(file2).rename(target2)

def check_pywintypes():
    try:
        import pywintypes
    except ModuleNotFoundError:
        base = Path(str(sys.executable)).parent.parent
        test = os.path.join(base, "lib", "win32", "lib", "pythoncom310.dll")
        if not os.path.exists(test):
            install_module('pypiwin32', 'pywintypes')
            pypiwin32_append_paths()
        else:
            pypiwin32_append_paths()
        try:
            import pywintypes
        except ModuleNotFoundError:
            print("Error installing pywintypes")


def install_addon():
    import bpy
    path = r'C:\Users\marco\blender-text-to-speech-offline\Text to Speech.zip'
    bpy.ops.preferences.addon_install(overwrite=True,
                                        target='DEFAULT',
                                        filepath=path,
                                        filter_folder=True,
                                        filter_python=False,
                                        filter_glob="*.py;*.zip")