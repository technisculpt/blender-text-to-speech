bl_info = {
    "name": "Text to Speech",
    "description": "turns text into speech",
    "author": "Mark Lagana",
    "version": (2, 1),
    "blender": (2, 92, 0), # tested up to 3.5.1
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

class PrefsError(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        if sys.platform == 'win32':
            layout.label(text="Pyttsx3 install failed. Open Blender in Administrator mode")
        else:
            layout.label(text="Pyttsx3 install failed")

if sys.platform != "darwin":
    try:
        import pyttsx3
        if sys.platform == 'win32':
            from .installers import windows
            importlib.reload(windows)
            windows.check_pywintypes()
    except ModuleNotFoundError:
        from . import install
        importlib.reload(install)

        install_result = install.install('pyttsx3')
        if install_result:
            print("Pyttsx3 installed")
            try:
                bpy.utils.unregister_class(PrefsError)
            except:
                pass

        else:
            bpy.utils.register_class(PrefsError)
            if sys.platform == 'win32':
                print("Pyttsx3 install failed. Open Blender in Administrator mode")
                
            else:
                print("Pyttsx3 install failed")

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
    operators.ConvertToTextStrip,
    operators.CreateTemplateStrip,
    ui.TextToSpeech_PT
)

def de_register_handlers():
    for handler in bpy.app.handlers.load_post:
        if handler.__name__ == 'btts_load_handler':
            bpy.app.handlers.load_post.remove(handler)

    for handler in bpy.app.handlers.save_pre:
        if handler.__name__ == 'btts_save_handler':
            bpy.app.handlers.save_pre.remove(handler)

def register_handlers():
    de_register_handlers()
    bpy.app.handlers.load_post.append(operators.btts_load_handler)
    bpy.app.handlers.save_pre.append(operators.btts_save_handler)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.text_to_speech = bpy.props.PointerProperty(type=ui.TextToSpeechSettings)
    register_handlers()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    try:
        bpy.utils.unregister_class(PrefsError)
    except:
        pass


    del bpy.types.Scene.text_to_speech
    de_register_handlers()
