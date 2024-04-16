# mark lagana 031524
#
# creates an audio strip from text 'testing' with;
# pitch 0.5, start frame 1, voice 0, in channel 2, with rate 140

import bpy
import text_to_speech.text_to_sound as tts

example_tts = tts.sound_strip_from_text(bpy.context, "test", 0.5, 1, 0, 2, 140)
print(example_tts)