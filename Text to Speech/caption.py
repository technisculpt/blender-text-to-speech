import importlib
import bpy
import os
import sys

from . import text_to_sound as tts
importlib.reload(tts)
from . import text_strip
importlib.reload(text_strip)

class Caption():
    
    def __init__(self, context, cc_type, name, text, start_time, end_time, voice, channel, pitch, rate, text_channel, tts_flag, text_flag, reconstruct=False):
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
        self.badpath = False

        if reconstruct: # reconstructing on fileload
            self.sound_strip = ""
        else:
            if tts_flag:
                self.sound_strip, self.filename = tts.sound_strip_from_text(context, text, pitch, self.frame_start, voice, channel, rate)
            if self.sound_strip == 'badpath':
                self.badpath = True
                exit()
            if text_flag:
                template = text_strip.check_for_template(context)
                if tts_flag:
                    f_end = self.sound_strip.frame_final_end
                else:
                    f_end = self.frame_start + context.scene.render.fps

                self.text_cap = text_strip.text_strip(context, text, self.frame_start, f_end, text_channel, template)

        if end_time.hours == -1 and not reconstruct:
            self.update_timecode()

    def update_timecode(self):
        self.start_time.frame_to_time(self.sound_strip.frame_start)
        self.end_time.frame_to_time(self.sound_strip.frame_final_end)
        self.frame_start = self.sound_strip.frame_start
    