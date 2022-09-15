import subprocess
from pathlib import Path
import os
import sys
import bpy
import importlib

def install(module, test):
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
    if test != module:
        try:
            importlib.import_module(test)
            print(f"{module} installed")
        except:
            print(f"Error installing {module}")



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
        return True
    except ModuleNotFoundError:
        base = Path(str(sys.executable)).parent.parent
        test = os.path.join(base, "lib", "win32", "lib", "pythoncom310.dll")
        if not os.path.exists(test):
            install('pypiwin32', 'pywintypes')
            pypiwin32_append_paths()
        else:
            pypiwin32_append_paths()
        try:
            import pywintypes
            print("pypiwin32 installed")
            return True
        except ModuleNotFoundError:
            print("Error installing pywintypes")
            return False

def install_pyttsx3():
    try:
        import pyttsx3
    except ModuleNotFoundError:
        install('pyttsx3', 'pyttsx3')
    check_pywintypes()


def install_addon():
    import bpy
    path = r'C:\Users\marco\blender-text-to-speech-offline\Text to Speech.zip'
    bpy.ops.preferences.addon_install(overwrite=True,
                                        target='DEFAULT',
                                        filepath=path,
                                        filter_folder=True,
                                        filter_python=False,
                                        filter_glob="*.py;*.zip")