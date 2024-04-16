from pathlib import Path
import importlib
import os

import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper # type: ignore
from bpy.types import Operator # type: ignore
from bpy.app.handlers import persistent # type: ignore
from bpy.props import EnumProperty # type: ignore

from . import blender_time as b_time
from . import caption as c
from .imports import txt as txt_import
from .imports import srt as srt_import
from .imports import sbv as sbv_import
from .imports import csv as csv_import
from .exports import txt as txt_export
from .exports import srt as srt_export
from .exports import sbv as sbv_export
from .exports import csv as csv_export
from . import char_encoding
from . import text_strip
importlib.reload(b_time)
importlib.reload(c)
importlib.reload(txt_import)
importlib.reload(srt_import)
importlib.reload(sbv_import)
importlib.reload(csv_import)
importlib.reload(txt_export)
importlib.reload(srt_export)
importlib.reload(sbv_export)
importlib.reload(csv_export)
importlib.reload(char_encoding)
importlib.reload(text_strip)

global_captions = []
template_strip = None

def remove_deleted_strips():
    global global_captions
    context = bpy.context
    scene = context.scene
    seq = scene.sequence_editor
    bpy.ops.sequencer.refresh_all()
    
    if not len(seq.sequences_all):
        global_captions.clear()

    it = 0
    end = len(global_captions)
    while(it < end):
        found = False
        for strip in seq.sequences_all:
            if global_captions[it].b_ID == strip.name:
                found = True
                global_captions[it].sound_strip = strip
        if not found:
            del global_captions[it]
            end -= 1
            it -= 1
        else:
            it += 1

def sort_strips_by_time():
    global global_captions
    bpy.ops.sequencer.refresh_all()
    for caption in global_captions:
        caption.update_timecode()
    
    global_captions.sort(key=lambda caption: caption.frame_start, reverse=False)

@persistent
def btts_load_handler(_scene):
    """ 
        btts_load_handler checks the blendfile for saved caption data and reconstructs the Caption instances
        this is for persistent data across sessions for accurate exporting of audio captions to text files (closed captions) as the strips are
        moved around and deleted. We store metadata of our Caption instances/objects in the blendfile and upon loading we reassociate the blender objects
        i.e sound and text strips with our custom python class instances (they become caption.b_obj_sound_strip & caption.b_obj_text_strip)
        the id of blender objects can change with undo/redo actions and across sessions so we assign the blender objects 'name' property
        to serve as a unique identifier for reassociation with our custom python class instances where the id is assigned to the 'b_ID' property
    """
    global global_captions
    if bpy.context.scene.text_to_speech.persistent_string:
        context = bpy.context
        scene = context.scene
        seq = scene.sequence_editor
        captions_raw = bpy.context.scene.text_to_speech.persistent_string.split('`')
        captions_raw.pop()
        _ = b_time.Time(-1, -1, -1, -1) # a flag to obtain timecodes from existing strips

        for caption in captions_raw:
            meta = caption.split('|')
            b_id = meta[0]
            c_type = int(meta[1])
            voice = int(meta[2])
            name = meta[3]
            text = meta[4]
            speech_channel = int(meta[5])
            text_channel = int(meta[6])
            pitch = float(meta[7])
            rate = float(meta[8])

            for strip in seq.sequences_all:
                if strip.name == b_id:
                    caption_strip = strip
                    break

            if caption_strip:
                new_cap = c.Caption(context, c_type, name, text, _, _, voice, speech_channel, text_channel, pitch, rate, True)
                new_cap.sound_strip = caption_strip
                new_cap.b_id = b_id
                new_cap.update_timecode()
                global_captions.append(new_cap)

@persistent
def btts_save_handler(_scene):
    """ 
        btts_save_handler saves all the caption instances data into the blendfile (like a database) as Blender doesn't save the state of our custom
        Python objects and pickle doesn't work if you have blender objects as class members. See btts_load_handler above for more info
    """
    global global_captions
    remove_deleted_strips()
    sort_strips_by_time()

    serialized_instances = ""
    for cap in global_captions:
        serialized_instances += f"{cap.b_ID}|{cap.cc_type}|{cap.voice}|{cap.name}|{cap.text}|{cap.speech_channel}|{cap.text_channel}|{cap.pitch}|{cap.rate}`"

    bpy.context.scene.text_to_speech.persistent_string = serialized_instances


def check_output_dir()->bool:
    relpath = False
    filepath_full = bpy.context.scene.render.filepath
    if (bpy.context.scene.render.filepath[0:2] == "//"):
        relpath = True
        filepath_full = bpy.path.abspath(bpy.context.scene.render.filepath)
    return not os.path.exists(filepath_full)

class TextToSpeechOperator(bpy.types.Operator):
    bl_idname = 'text_to_speech.speak'
    bl_label = 'speak op'
    bl_options = {'INTERNAL'}
    bl_description = "turns text into audio strip at current playhead"

    def execute(self, context):

        @classmethod
        def poll(cls, context): 
            props = context.scene.voronpi
            return bool(props.string_field.strip()) and context.area.type != 'SEQUENCE_EDITOR'
        
        global global_captions
        seconds = bpy.context.scene.frame_current / bpy.context.scene.render.fps
        props = context.scene.text_to_speech

        if check_output_dir():
            self.report({'INFO'}, "Output path doesn't exist")
            return {'CANCELLED'}
        else:
            start_t = b_time.Time(0, 0, seconds, 0)
            end_t = b_time.Time(-1, -1, -1, -1)
            new_cap = c.Caption(context, 0, "", props.string_field, start_t, end_t, props.voice_enum,
                              props.speech_channel, None, props.pitch, props.rate, False)
            global_captions.append(new_cap)
            self.report({'INFO'}, "FINISHED")
            return {'FINISHED'}

class ClosedCaptionSet(): # translates cc files into a list of caption.Captions
    captions = []
    people = []

    def get(self):
        return(self.captions)

    def arrange_captions_by_time(self, with_text=False): # when timecode not provided
        bpy.ops.sequencer.select_all(action='DESELECT')
        frame_pointer = self.captions[0].sound_strip.frame_duration + bpy.context.scene.render.fps
        bpy.context.scene.tool_settings.sequencer_tool_settings.overlap_mode = 'SHUFFLE'

        for caption in range(1, len(self.captions)):
            
            self.captions[caption].sound_strip.select = True
            if with_text:
                self.text_caps[caption].select = True
            bpy.ops.transform.seq_slide(value=(frame_pointer, 0.0))
            # TODO there is a minor bug here where seq_slide doesn't always move the strips by exactly frame_pointer + 1sec
            self.captions[caption].sound_strip.select = False
            if with_text:
                self.text_caps[caption].select = False
            frame_pointer += self.captions[caption].sound_strip.frame_duration + bpy.context.scene.render.fps

            
    def __init__(self, context, text, filename, _voice, pitch, rate, speech_channel, text_channel, speech_flag, text_flag):
        ext = filename[-3:len(filename)]
        self.finished = False

        if ext == 'csv':
            self.captions = csv_import.import_cc(context, filename)
            if len(self.captions) > 0:
                self.finished = True
            else:
                print("csv file error")
                self.finished = False

        elif ext == 'txt':
            self.captions, self.text_caps = txt_import.import_cc(context, text, _voice, pitch, rate, speech_channel,
                                                text_channel, speech_flag, text_flag)

            if self.text_caps:
                self.arrange_captions_by_time(with_text=True)
            else:
                self.arrange_captions_by_time()

            self.finished = True
            
        elif ext == 'srt':
            self.captions = srt_import.import_cc(context, text, _voice, pitch, rate, speech_channel,
                                                text_channel, speech_flag, text_flag)
            self.finished = True

        elif ext == 'sbv':
            self.captions = sbv_import.import_cc(context, text, _voice, pitch, rate, speech_channel,
                                                text_channel, speech_flag, text_flag)
            self.finished = True


class ImportClosedCapFile(Operator, ImportHelper):
    bl_idname = "_import.cc_file"
    bl_label = "Import CC Data"

    codec: EnumProperty(  # type: ignore
        name="File Encoding",
        description="Choose File Encoding",
        items = char_encoding.items,
        default='95')

    tts_flag : bpy.props.BoolProperty( # type: ignore
        name="Text to speech",
        description="Option to create text to speech audio strips",
        default=True)

    text_strip_flag : bpy.props.BoolProperty( # type: ignore
        name="Text strips",
        description="Option to create text strips",
        default=False)

    def execute(self, context):

        global global_captions
        f = Path(bpy.path.abspath(self.filepath))
        props = context.scene.text_to_speech

        if f.exists():
            enc = char_encoding.items[int(self.codec)][1]
            captions =  ClosedCaptionSet(context, f.read_text(encoding=enc).split("\n"), self.filepath,
                                        props.voice_enum, props.pitch, props.rate,
                                        props.speech_channel, props.text_channel, self.tts_flag, self.text_strip_flag)
            if captions.finished:
                global_captions += captions.get()
                return {'FINISHED'}

            else:
                self.report({'INFO'}, 'Please try .txt, .srt, .sbv or csv file')
                return {'CANCELLED'}

class LoadFileButton(Operator):
    bl_idname = 'text_to_speech.load'
    bl_label = 'load op'
    bl_options = {'INTERNAL'}
    bl_description = "loads closed captions from txt, srt or sbv file"
    
    def execute(self, context):
        if check_output_dir():
            self.report({'INFO'}, "Output path doesn't exist")
            return {'CANCELLED'}
        
        bpy.ops._import.cc_file('INVOKE_DEFAULT')
        return {'FINISHED'}

def export_cc_file(context, filepath, file_type):
    global global_captions
    remove_deleted_strips()
    sort_strips_by_time()

    if file_type == 'txt':
        return(txt_export.export(filepath, global_captions))

    if file_type == 'srt':
        return(srt_export.export(filepath, global_captions))

    if file_type == 'sbv':
        return(sbv_export.export(filepath, global_captions))

    if file_type == 'csv':
        return(csv_export.export(filepath, global_captions))

class ExportFileName(Operator, ExportHelper):
    bl_idname = "_export.cc_file"
    bl_label = "Export CC Data"
    filename_ext = ""
    
    filetype: EnumProperty( # type: ignore
        name="Filetype",
        description="Choose File Type",
        items=(
            ("txt", "txt", "text file"),
            ("srt", "srt", "srt file"),
            ("sbv", "sbv", "sbv file"),
            ("csv", "csv", "csv file"),
        ),
        default="txt",
    )
  
    def execute(self, context):
        if export_cc_file(context, self.filepath, self.filetype):
            return {'FINISHED'}

        else:
            self.report({'INFO'}, 'File already exists.')
            return {'CANCELLED'}

class ExportFileButton(Operator):
    bl_idname = 'text_to_speech.export'
    bl_label = 'export op'
    bl_options = {'INTERNAL'}
    bl_description = "exports closed caption file to a filepath"
    
    def execute(self, context):
        bpy.ops._export.cc_file('INVOKE_DEFAULT')
        return {'FINISHED'} 

class ConvertToTextStrip(Operator):
    bl_idname = 'text_to_speech.speech_to_strip'
    bl_label = 'convert to text strip'
    bl_options = {'INTERNAL'}
    bl_description = "convert selected audio captions to text strips"
    
    def execute(self, context):

        if check_output_dir():
            self.report({'INFO'}, "Output path doesn't exist")
            return {'CANCELLED'}

        global global_captions
        global template_strip
        remove_deleted_strips()
        props = context.scene.text_to_speech
        template = text_strip.check_for_template(context)
        for cap in global_captions:
            if cap.sound_strip.select:
                text_strip.text_strip(context, cap.text, cap.sound_strip.frame_start,
                                    cap.sound_strip.frame_final_end, props.text_channel, template)
        return {'FINISHED'}

class CreateTemplateStrip(Operator):
    bl_idname = 'text_to_speech.create_template'
    bl_label = 'create template text strip'
    bl_options = {'INTERNAL'}
    bl_description = "create template for text strip creation"
    
    def execute(self, context):

        if check_output_dir():
            self.report({'INFO'}, "Output path doesn't exist")
            return {'CANCELLED'}
        
        global template_strip
        _scene = context.scene
        tts_props = context.scene.text_to_speech

        if not _scene.sequence_editor:
            _scene.sequence_editor_create()
        seq = _scene.sequence_editor

        f_start = context.scene.frame_current
        f_end = f_start + context.scene.render.fps

        template_strip = seq.sequences.new_effect(
            name="Template_strip",
            type='TEXT',
            frame_start=f_start,
            frame_end=f_end,
            channel=tts_props.text_channel)

        return {'FINISHED'}
