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

class InitialPanel(AddonPreferences):
    bl_idname = __package__

    password: StringProperty(
        name="User Password:",
        subtype='PASSWORD',
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Installing addon may take a moment for libraries to install:")
        layout.prop(self, "password")
        layout.operator('text_to_speech.addon_prefs_feedback', text='Install addon')


class OBJECT_OT_install_addon(Operator):
    bl_idname = "text_to_speech.addon_prefs_feedback"
    bl_label = "Add-on Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        addon_prefs = context.preferences.addons[__package__].preferences
        print(addon_prefs.password)
        bpy.utils.unregister_class(InitialPanel)
        bpy.utils.register_class(FeedbackPanel)
        if install.install('pyttsx3'):
            register_classes()
            bpy.utils.unregister_class(FeedbackPanel)
            bpy.utils.register_class(SuccessPanel)
        else:
            bpy.utils.unregister_class(FeedbackPanel)
            bpy.utils.register_class(FailurePanel)
        return {'FINISHED'}

class FeedbackPanel(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Installing addon...")

class SuccessPanel(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Addon successfully installed")

class FailurePanel(AddonPreferences):
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

