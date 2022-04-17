import subprocess
from pathlib import Path
import os
import sys
import bpy


def install(module):

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
        exec(f"import {module}")
        print(f"{module} installed")
    except:
        print(f"Error installing {module}")

def pypiwin32_cleanup():

    py_exec = str(sys.executable)
    base = Path(py_exec).parent.parent
    print(base)
    #lib = os.path.join(base, "lib", "win32", "lib")
    #sys.path.append(lib)
    #lib = os.path.join(base, "lib", "win32")
    #sys.path.append(lib) # _win32sysloader.cp310-win_amd64.pyd
    #file1 = os.path.join(base, "lib", "pywin32_system32", "pythoncom310.dll")
    #file2 = os.path.join(base, "lib", "pywin32_system32", "pywintypes310.dll")
    #target1 = os.path.join(base, "lib", "pythoncom310.dll")
    #target2 = os.path.join(base, "lib", "pywintypes310.dll")
    #Path(file1).rename(target1)
    #Path(file2).rename(target2)