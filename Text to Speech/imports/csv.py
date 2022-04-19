import sys
import os
import csv
import bpy
from pathlib import Path

from .. import blender_time as b_time
from .. import caption as c

def import_cc(context, file):
    print(".csv file detected")

    captions = []

    rows = []
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            if len(row) == 16:
                rows.append(row)
    
    if header[0] == 'cc_type':
        
        for row in rows:
            
            cc_type = int(row[0])
            voice = int(row[1])
            cc_name = row[2]
            cc_text = row[3]
            hrs_start = int(row[4])
            min_start = int(row[5])
            sec_start = int(row[6])
            ms_start = int(row[7])
            hrs_end = int(row[8])
            min_end = int(row[9])
            sec_end = int(row[10])
            ms_end = int(row[11])
            frame_start = int(row[12])
            channel = int(row[13])
            pitch = float(row[14])
            rate = int(row[15])
            start_time = b_time.Time(hrs_start, min_start, sec_start, ms_start)
            end_time = b_time.Time(hrs_end, min_end, sec_end, ms_end)
            cap = c.Caption(context, cc_type, cc_name, cc_text, start_time, end_time, voice, channel, pitch, rate)
            cap.sound_strip.frame_start = frame_start
            captions.append(cap)
        
        return(captions)

    else:
        return(-1)