import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

import importlib

from . import install
from . import operators
from . import ui
importlib.reload(install)
importlib.reload(operators)
importlib.reload(ui)

class InstallAddonPreferences(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Installing addon may take a moment for libraries to install")
        layout.operator('text_to_speech.addon_prefs_example', text='Install addon')

class OBJECT_OT_addon_prefs_example(Operator):
    """Display example preferences"""
    bl_idname = "text_to_speech.addon_prefs_example"
    bl_label = "Add-on Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.utils.unregister_class(InstallAddonPreferences)
        bpy.utils.register_class(InstallingFeedbackAddonPreferences)
        if install.install('pyttsx3'):
            register_classes()
            bpy.utils.unregister_class(InstallingFeedbackAddonPreferences)
            bpy.utils.register_class(SuccessFeedbackAddonPreferences)
        else:
            bpy.utils.unregister_class(InstallingFeedbackAddonPreferences)
            bpy.utils.register_class(FailureFeedbackAddonPreferences)
        return {'FINISHED'}

class InstallingFeedbackAddonPreferences(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Installing addon...")

class SuccessFeedbackAddonPreferences(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Addon successfully installed")

class FailureFeedbackAddonPreferences(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Problem installing addon, please check console")

classes = (
    ui.TextToSpeechSettings,
    operators.TextToSpeechOperator,
    operators.ImportClosedCapFile,
    operators.LoadFileButton,
    operators.ExportFileName,
    operators.ExportFileButton,
    operators.ConvertToTextStrip,
    operators.CreateTemplateStrip,
    ui.TextToSpeech_PT,
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

def register_classes():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.text_to_speech = bpy.props.PointerProperty(type=ui.TextToSpeechSettings)
    register_handlers()

