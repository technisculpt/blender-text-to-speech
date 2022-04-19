import importlib
import bpy
import os
import sys

from . import text_to_sound as tts
importlib.reload(tts)

class Caption():
    
    def __init__(self, context, cc_type, name, text, start_time, end_time, voice, channel, pitch, rate, reconstruct=False):
        self.cc_type = cc_type # 0 : default, 1 : person, 2 : event
        self.voice = voice
        self.name = name
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
        self.frame_start = start_time.time_to_frame()
        self.channel = channel
        self.pitch = pitch
        self.rate = rate

        if reconstruct: # reconstructing on fileload
            self.sound_strip = ""
        else:
            if self.frame_start != -1:
                self.sound_strip, self.filename = tts.sound_strip_from_text(context, text, pitch, self.frame_start, voice, channel, rate)
            else:
                self.sound_strip, self.filename = tts.sound_strip_from_text(context, text, pitch, 0, voice, channel, rate)
            

    def update_timecode(self):
        self.start_time.frame_to_time(self.sound_strip.frame_start)
        self.end_time.frame_to_time(self.sound_strip.frame_final_end)
        self.current_seconds = self.sound_strip.frame_start / bpy.context.scene.render.fps
        self.frame_start = self.sound_strip.frame_start