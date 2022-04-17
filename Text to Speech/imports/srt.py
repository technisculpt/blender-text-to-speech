import sys
import os

import bpy

from .. import blender_time as b_time
from .. import caption as c

def import_cc(context, text, gender, pitch, rate):
    print(".srt file detected")
    captions = []
    line_counter = 0
    cc_text = ""
    cc_type = 1
    start_time = 0
    end_time = 0

    for line in text:

        if len(line) > 0:

            if line.find('-->') != -1 and line[0].isnumeric(): # timecode
                start = line.split("-->")[0]
                end = line.split("-->")[1]
                hrs_start = int(start.split(":")[0])
                min_start = int(start.split(":")[1])
                sec_start = int(start.split(":")[2].split(',')[0])
                ms_start = int(start.split(":")[2].split(',')[1])

                hrs_end = int(end.split(":")[0])
                min_end = int(end.split(":")[1])
                sec_end = int(end.split(":")[2].split(',')[0])
                ms_end = int(end.split(":")[2].split(',')[1])

                start_time = b_time.Time(hrs_start, min_start, sec_start, ms_start)
                end_time = b_time.Time(hrs_end, min_end, sec_end, ms_end)

            elif line[0:2].find('>>') != -1: # person
                cc_type = 1
                cc_name = line[2:len(line)].split(":")[0]
                text_tmp = line[2:len(line)].split(":")[1]
                cc_text = text_tmp[1:len(text_tmp)]

            elif line[0] == '[': # event
                cc_type = 2
                cc_name = ''
                cc_text = line.split('[')[1].split(']')[0]
            
            elif line.isnumeric(): # cc number
                pass

            elif(len(line) > 1): # plain text line
                
                if len(cc_text) == 0: # no previous line
                    cc_name = "noname"
                    cc_type = 0
                    cc_text = line

                else: # second line
                    cc_text += " " + line

        else: # len(line == 0) equivalent of '\n'
            if len(cc_text) > 0:
                captions.append(c.Caption(context, cc_type, cc_name, cc_text, start_time, end_time, gender, 1, pitch, rate))
                cc_text = ""

        line_counter += 1
        if line_counter == len(text): # on exit
            if len(cc_text) > 0:
                captions.append(c.Caption(context, cc_type, cc_name, cc_text, start_time, end_time, gender, 1, pitch, rate))
        
    return(captions)