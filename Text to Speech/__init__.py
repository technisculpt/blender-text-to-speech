bl_info = {
    "name": "Text to Speech",
    "description": "turns text into speech",
    "author": "Mark Lagana",
    "version": (1, 0),
    "blender": (3, 1, 0),
    "location": "SEQUENCE_EDITOR > UI > Text to Speech",
    "warning": "",
    "doc_url": "https://github.com/technisculpt/blender-text-to-speech",
    "support": "COMMUNITY",
    "category": "Sequencer",
}

from numbers import Number
from re import T 
import importlib
import bpy
import sys
import os
from pathlib import Path

try:
    import pyttsx3
except ModuleNotFoundError:
    from . import install
    importlib.reload(install)
    install.install('pyttsx3')

try:
    import pypiwin32
except ModuleNotFoundError:
    from . import install
    importlib.reload(install)
    install.install('pypiwin32')

    if sys.platform == "win32":
        py_exec = str(sys.executable)
        base = Path(py_exec).parent.parent
        lib = os.path.join(base, "lib", "win32", "lib")
        sys.path.append(lib) # pywintypes310.dll
        lib = os.path.join(base, "lib", "win32")
        sys.path.append(lib) # _win32sysloader.cp310-win_amd64.pyd
        file1 = os.path.join(base, "lib", "pywin32_system32", "pythoncom310.dll")
        file2 = os.path.join(base, "lib", "pywin32_system32", "pywintypes310.dll")
        target1 = os.path.join(base, "lib", "pythoncom310.dll")
        target2 = os.path.join(base, "lib", "pywintypes310.dll")
        Path(file1).rename(target1)
        Path(file2).rename(target2)

from . import operators
importlib.reload(operators)
from . import ui
importlib.reload(ui)

classes = (
    ui.TextToSpeechSettings,
    ui.TextToSpeech_PT,
    operators.TextToSpeechOperator,
    operators.ImportClosedCapFile,
    operators.LoadFileButton,
    operators.ExportFileName,
    operators.ExportFileButton,
    )

def register_handlers():
    for handler in bpy.app.handlers.load_post:
        if handler.__name__ == 'btts_load_handler':
            bpy.app.handlers.load_post.remove(handler)

    for handler in bpy.app.handlers.save_pre:
        if handler.__name__ == 'btts_save_handler':
            bpy.app.handlers.save_pre.remove(handler)

    bpy.app.handlers.load_post.append(operators.btts_load_handler)
    bpy.app.handlers.save_pre.append(operators.btts_save_handler)


def de_register_handlers():
    for handler in bpy.app.handlers.load_post:
        if handler.__name__ == 'btts_load_handler':
            bpy.app.handlers.load_post.remove(handler)

    for handler in bpy.app.handlers.save_pre:
        if handler.__name__ == 'btts_save_handler':
            bpy.app.handlers.save_pre.remove(handler)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.text_to_speech = bpy.props.PointerProperty(type=ui.TextToSpeechSettings)
    register_handlers()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.text_to_speech
    de_register_handlers()

if __name__ == '__main__':
    register()