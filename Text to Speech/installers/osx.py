import subprocess
from pathlib import Path
import os
import sys
import bpy

def install(module):

    if bpy.app.version < (2, 92, 0):
        py_exec = bpy.app.binary_path_python
        py_exec = os.path.join(Path(py_exec).parent.parent, "lib", "python3.7")
        # this throws permission error 13
        # maybe related to: https://developer.blender.org/T72605
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

def test():
    import pyttsx3
    import os
    text = "test"
    output_name = os.path.join(bpy.context.scene.render.filepath, text + ".wav")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[11].id)
    engine.setProperty('rate', 200)
    engine.save_to_file(text, output_name)
    engine.runAndWait()

if __name__ == "__main__":
    # cd /Applications/Blender.app/Content/MacOs
    # ./Blender -b -P script.py
    # Applications/Blender.app/Contents/Recourses/2.83/python
    install('pyttsx3')
