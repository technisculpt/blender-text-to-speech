import bpy
from sys import platform
import importlib

class TextToSpeechSettings(bpy.types.PropertyGroup):
    persistent_string : bpy.props.StringProperty(name='Persistent String')
    string_field : bpy.props.StringProperty(name='Text')

    if platform == "darwin":
        from .voices import osx
        importlib.reload(osx)
        voice_enumerator : bpy.props.EnumProperty(
                    name = "",
                    description = "gender options",
                    items= osx.voices)

    elif platform == "linux":
        from .voices import linux
        importlib.reload(linux)
        voice_enumerator : bpy.props.EnumProperty(
            name = "",
            description = "gender options",
            items= linux.voices)

    else:
        voice_enumerator : bpy.props.EnumProperty(
            name = "",
            description = "gender options",
            items=[ ('0',"David - Male - English (US)",""),
                    ('1',"Zira - Female - English (US)","")])

    pitch : bpy.props.FloatProperty(
        name="Pitch",
        description="Text to Speech Pitch",
        default=1.0,
        min=0.1, max=10.0,
        )

    rate : bpy.props.IntProperty(
        name="Rate",
        description="Text to Speech Rate",
        default=140,
        min=1, max=1000,
        )   

class TextToSpeech_PT(bpy.types.Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_label = 'Text To Speech'
    bl_category = 'Text To Speech'
    bl_idname = 'SEQUENCER_PT_text_to_speech'

    def draw(self, context):

        layout = self.layout
        scene = context.scene.text_to_speech

        col = layout.column(align=True)
        col.use_property_split = True
        col.prop(scene, 'voice_enumerator', text='Voice')

        col = layout.column(align=True)
        col.use_property_split = True
        col.prop(scene, 'rate', text='Rate')
        
        col = layout.column(align=True)
        col.use_property_split = True
        col.prop(scene, 'pitch', text='Pitch')

        box = layout.box()
        col = box.column(align=True)
        col.use_property_split = False
        col.prop(scene, 'string_field', text = '')
        col.operator('text_to_speech.speak', text = 'Text to Speech', icon='ADD')

        col = layout.column()
        col.use_property_split = True
        subrow = layout.row(align=True)
        subrow.operator('text_to_speech.load', text = 'Load Captions File', icon='IMPORT')

        col = layout.column()
        col.use_property_split = True
        subrow = layout.row(align=True)
        subrow.operator('text_to_speech.export', text = 'Export Captions File', icon='EXPORT')


