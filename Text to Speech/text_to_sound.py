import pyttsx3
import os
import sys
import time
import bpy
from sys import platform
import string
import subprocess

not_allowed = ['/', '"', '\'']
if platform == "win32":
    not_allowed = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
elif platform == "linux":
    not_allowed = ['/', '"', '\'', " "]

def mac_engine(_text, _voice, _rate, _path):
    subprocess.call(["say", _text, "-o", _path, f"--rate={_rate}", "-v", _voice])

def engine(_text, _voice, _rate, _path):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[int(_voice)].id)
    engine.setProperty('rate', int(_rate))
    engine.save_to_file(_text, _path)
    engine.runAndWait()


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

    if sys.platform == "darwin":
        mac_engine(text, voice, rate, output_name)
    else:
        engine(text, voice, rate, output_name)


    _scene = context.scene
    if not _scene.sequence_editor:
        _scene.sequence_editor_create()
    seq = _scene.sequence_editor

    if relpath:
        obj = seq.sequences.new_sound(identifier, filepath=bpy.path.relpath(output_name), channel=audio_channel, frame_start=start_frame)
    else:
        obj = seq.sequences.new_sound(identifier, output_name, channel=audio_channel, frame_start=start_frame)

    if bpy.app.version >= (3, 3, 0):
        obj.speed_factor = pitch
    else:
        obj.pitch = pitch

    return obj, identifier