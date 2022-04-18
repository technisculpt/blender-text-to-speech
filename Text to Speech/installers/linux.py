import subprocess
from pathlib import Path
import os
import sys
import bpy

def install(module):

    if bpy.app.version < (2, 92, 0):
        py_exec = bpy.app.binary_path_python
        subprocess.call([str(py_exec), "-m", "ensurepip", "--user"])
        subprocess.call([str(py_exec), "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.call([str(py_exec),"-m", "pip", "install", "--user", module])
    else:
        py_exec = str(sys.executable)
        lib = os.path.join(Path(py_exec).parent.parent, 'lib', 'python3.10')
        subprocess.call([py_exec, "-m", "ensurepip", "--user" ])
        subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "pip" ])
        subprocess.call([py_exec,"-m", "pip", "install", f"--target={str(lib)}", module])
    try:
        exec(f"import {module}")
        print(f"{module} installed")
    except:
        print(f"Error installing {module}")

def apt_install_deps():

    subprocess.check_call(['sudo', 'apt', 'install', '-y', 'espeak'],
     stdout=open(os.devnull,'wb'), stderr=subprocess.STDOUT)
    subprocess.check_call(['sudo', 'apt', 'install', '-y', 'ffmpeg'],
     stdout=open(os.devnull,'wb'), stderr=subprocess.STDOUT)
    subprocess.check_call(['sudo', 'apt', 'install', '-y', 'libespeak1'],
     stdout=open(os.devnull,'wb'), stderr=subprocess.STDOUT) 