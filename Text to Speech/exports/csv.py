import sys
import os
import csv
import bpy

from . import export_helper as lib

header = ["cc_type", "accent", "name", "text",
        "start_time_hr", "start_time_min", "start_time_sec", "start_time_ms",
        "end_time_hr", "end_time_min", "end_time_sec", "end_time_ms",
        "start_frame", "channel", "pitch"]

def export(filepath, captions):
    try:
        with open(f"{filepath}.csv", "x") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(header)
            data = []

            for caption in range(len(captions)):

                cap = []
                cap.append(captions[caption].cc_type)
                cap.append(captions[caption].accent)
                cap.append(captions[caption].name)
                cap.append(captions[caption].text)
                cap.append(captions[caption].start_time.hours)
                cap.append(captions[caption].start_time.minutes)
                cap.append(captions[caption].start_time.seconds)
                cap.append(captions[caption].start_time.milliseconds)
                cap.append(captions[caption].end_time.hours)
                cap.append(captions[caption].end_time.minutes)
                cap.append(captions[caption].end_time.seconds)
                cap.append(captions[caption].end_time.milliseconds)
                cap.append(captions[caption].frame_start)
                cap.append(captions[caption].channel)
                cap.append(captions[caption].pitch)
                data.append(cap)

            csvwriter.writerows(data) # 5. write the rest of the data

        return(True)

    except FileExistsError:
        print("File already exists")
        return(False)