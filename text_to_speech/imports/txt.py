import sys
import os
import importlib

import bpy

from .. import blender_time as b_time
from .. import caption as c
importlib.reload(b_time)
importlib.reload(c)


def import_cc(context, text, gender, pitch, rate, channel, text_channel, tts_flag, text_flag):
    print(".txt file detected")
    captions = []
    line_counter = 0
    cc_text = ""
    cc_type = 1
    if text_flag:
        text_caps = []
    else:
        text_caps = False

    for line in text:
        if len(line) > 0:
            if line[0:2].find('>>') != -1: # person
                cc_type = 1
                cc_name = line[2:len(line)].split(":")[0]
                text_tmp = line[2:len(line)].split(":")[1]
                cc_text = text_tmp[1:len(text_tmp)]

            elif line[0] == '[': # event
                cc_type = 2
                cc_name = ''
                cc_text = line.split('[')[1].split(']')[0]
            
            else: # plain text line

                if len(cc_text) == 0: # no previous line
                    cc_name = "noname"
                    cc_type = 0
                    cc_text = line

                else: # second line
                    cc_text += " " + line
        
        else: # len(line == 0) equivalent of '\n'
            tts = c.Caption(context, cc_type, cc_name, cc_text,
                                b_time.Time(-1, -1, -1, -1), b_time.Time(-1, -1, -1, -1),
                                gender, channel, pitch, rate, text_channel, tts_flag, text_flag)
            captions.append(tts)
            if text_flag:
                text_caps.append(tts.text_cap)
            cc_text = ""

        line_counter += 1
        if line_counter == len(text): # on exit
            if len(cc_text) > 0:
                tts = c.Caption(context, cc_type, cc_name, cc_text,
                                    b_time.Time(-1, -1, -1, -1), b_time.Time(-1, -1, -1, -1),
                                    gender, channel, pitch, rate, text_channel, tts_flag, text_flag)
                captions.append(tts)
                if text_flag:
                    text_caps.append(tts.text_cap)

    return(captions, text_caps)