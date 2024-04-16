import importlib
import bpy
import os
import sys

from . import text_to_sound as tts
importlib.reload(tts)
from . import text_strip
importlib.reload(text_strip)

class Caption():
    
    def __init__(self, context, cc_type, name, text, start_time, end_time, voice, speech_channel, text_channel, pitch, rate, reconstruct=False):
        self.cc_type = cc_type # 0 : default, 1 : person, 2 : event
        self.voice = voice # voice settings vary across operating systems
        self.name = name # optional name for the actor
        self.text = text # text of the caption could become a sound or text strip
        self.start_time = start_time
        self.end_time = end_time
        self.frame_start = start_time.time_to_frame()
        self.speech_channel = speech_channel
        self.text_channel = text_channel
        self.pitch = pitch
        self.rate = rate

        if reconstruct: # reconstructing on fileload
            self.b_obj_sound_strip = None
        else:
            if speech_channel:
                self.b_obj_sound_strip, self.b_ID = tts.sound_strip_from_text(context, text, pitch, self.frame_start, voice, speech_channel, rate)
            if text_channel:
                template = text_strip.check_for_template(context)
                if speech_channel:
                    frame_end = self.b_obj_sound_strip.frame_final_end
                else:
                    frame_end = self.frame_start + context.scene.render.fps

                self.b_obj_text_strip = text_strip.text_strip(context, text, self.frame_start, frame_end, text_channel, template)

        if end_time.hours == -1 and not reconstruct:
            self.update_timecode() # fill out timecodes for the operator which uses playhead for po

    def update_timecode(self):
        self.start_time.frame_to_time(self.b_obj_sound_strip.frame_start)
        self.end_time.frame_to_time(self.b_obj_sound_strip.frame_final_end)
        self.frame_start = self.b_obj_sound_strip.frame_start
    