from datetime import timedelta
import bpy

class Time():
    def __init__(self, hours=0, minutes=0, seconds=0, milliseconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds

    def time_to_frame(self):
        if self.hours == -1:
            return 0
        else:
            total_seconds = ((self.hours * 3600)
                            + (self.minutes * 60)
                            + self.seconds
                            + (self.milliseconds/1000))
                            
        return int(total_seconds * bpy.context.scene.render.fps)

    def frame_to_time(self, frames):
        td = timedelta(seconds=(frames / bpy.context.scene.render.fps))

        if (td.seconds/3600 >= 1):
            self.hours = int(td.seconds/3600)
        else:
            self.hours = 0

        if (td.seconds/60 >= 1):
            self.minutes = int(td.seconds/60) % 60
        else:
            self.minutes = 0
        if (td.seconds >= 1): 
            if (td.seconds >= 60):
                self.seconds = td.seconds % 60
            else:
                self.seconds = td.seconds
        else:
            self.seconds = 0
        self.milliseconds = int((td.microseconds / 1000) % 1000)
        return