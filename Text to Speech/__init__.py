bl_info = {
    "name": "Text to Speech",
    "description": "turns text into speech",
    "author": "Mark Lagana",
    "version": (1, 0),
    "blender": (3, 10, 0),
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

from . import operators
importlib.reload(operators)
from . import ui
importlib.reload(ui)
from . import preferences
importlib.reload(preferences)
from .installers import windows
importlib.reload(windows)

libraries_installed = False

if sys.platform != "darwin":
    try:
        import pyttsx3
        if sys.platform == 'win32':
            windows.check_pywintypes()
        libraries_installed = True
    except ModuleNotFoundError:
        bpy.utils.register_class(preferences.OBJECT_OT_install_addon)
        bpy.utils.register_class(preferences.InitialPanel)

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

install_classes = (
    preferences.OBJECT_OT_install_addon,
    preferences.InitialPanel,
    preferences.FeedbackPanel,
    preferences.SuccessPanel,
    preferences.FailurePanel
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
    if sys.platform == "darwin" or libraries_installed:
        for cls in classes:
            bpy.utils.register_class(cls)

        bpy.types.Scene.text_to_speech = bpy.props.PointerProperty(type=ui.TextToSpeechSettings)
        register_handlers()

def unregister():
    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except:
            print("Couldn't unreg class: " + str(cls))

    try:
        del bpy.types.Scene.text_to_speech
    except:
        print("Couldn't unreg bpy.types.Scene.text_to_speech")

    de_register_handlers()

    for cls in install_classes:
        try:
            bpy.utils.unregister_class(cls)
        except:
            print("Couldn't unreg install class: " + str(cls))