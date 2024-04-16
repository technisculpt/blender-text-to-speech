# mark lagana 031524
#
# creates a simple text strip in the sequencer in one line
# it's the same as calling:
#
# bpy.ops.sequencer.effect_strip_add(type='TEXT', frame_start=1, frame_end=11, channel=2)
# bpy.context.active_sequence_strip.name = "test text strip from frame one to eleven, on channel two"
#
# however we can also programatically create strips from a template strip, see text_from_template.py 

import bpy
import text_to_speech.text_strip as text_strip

example_text_strip = text_strip.text_strip(bpy.context, "test text strip from frame one to eleven, on channel two", 1, 11, 2, template_strip=None)
example_text_strip.location.x += 0.01