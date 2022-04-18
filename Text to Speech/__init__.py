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
    install.install('pyttsx3', 'pyttsx3')

if sys.platform.startswith("linux"):
    from .installers import linux
    importlib.reload(linux)
    # TODO make this only run if needed
    linux.apt_install_deps()

if sys.platform == "win32":
    try:
        import pywintypes
    except ModuleNotFoundError:
        from .installers import windows
        importlib.reload(windows)
        base = Path(str(sys.executable)).parent.parent
        test = os.path.join(base, "lib", "win32", "lib", "pythoncom310.dll")
        if not os.path.exists(test):
            windows.install('pypiwin32', 'pywintypes')
            windows.pypiwin32_append_paths()
        else:
            windows.pypiwin32_append_paths()
        try:
            import pywintypes
            print("pypiwin32 installed")
        except ModuleNotFoundError:
            print("Error installing pywintypes")
    

from . import operators
importlib.reload(operators)
from . import ui
importlib.reload(ui)

classes = (
    ui.TextToSpeechSettings,
    operators.TextToSpeechOperator,
    operators.ImportClosedCapFile,
    operators.LoadFileButton,
    operators.ExportFileName,
    operators.ExportFileButton,
    ui.TextToSpeech_PT,
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