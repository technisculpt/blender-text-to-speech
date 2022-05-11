import pyttsx3
import os
import time
import bpy
from sys import platform
import string

not_allowed = ['/', '"', '\'']
if platform == "win32":
    not_allowed = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
elif platform == "linux":
    not_allowed = ['/', '"', '\'', " "]

def sound_strip_from_text(context, text, pitch, start_frame, voice, audio_channel, rate):

    tmp_ident = text[0:45]
    
    text_ident = ""
    for char in tmp_ident:
        if char in not_allowed:
            pass
        else:
            text_ident += char

    relpath = False
    filepath_full = bpy.context.scene.render.filepath
    if (bpy.context.scene.render.filepath[0:2] == "//"):
        relpath = True
        filepath_full = bpy.path.abspath(bpy.context.scene.render.filepath)

    time_now = time.strftime("%Y%m%d%H%M%S")
    identifier = f"{text_ident}{time_now}"
    output_name = os.path.join(filepath_full, identifier + ".aiff")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[int(voice)].id)
    engine.setProperty('rate', int(rate))
    engine.save_to_file(text, output_name)
    engine.runAndWait()

    _scene = context.scene
    if not _scene.sequence_editor:
        _scene.sequence_editor_create()
    seq = _scene.sequence_editor

    if relpath:
        obj = seq.sequences.new_sound(identifier, filepath=bpy.path.relpath(output_name), channel=audio_channel, frame_start=start_frame)
    else:
        obj = seq.sequences.new_sound(identifier, output_name, channel=audio_channel, frame_start=start_frame)

    obj.pitch = pitch
    
    return obj, identifier