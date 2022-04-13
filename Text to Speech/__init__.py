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

# Successfully installed pypiwin32-223 pywin32-303
# mv blender_python/lib/win32/lib/pywintypes310.dll -> blender_python/lib
# maybe mv blender_python/lib/win32/lib/pythoncom310.dll -> blender_python/lib
# mv blender_python/_win32sysloader.cp310-win_amd64.pyd -> blender_python/lib

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