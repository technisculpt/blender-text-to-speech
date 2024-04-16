import os
import time
import sys
from sys import platform
import subprocess
import pyttsx3
import bpy

max_bytes = 30

not_allowed = ['/', '"', '\'']
if platform == "win32":
    not_allowed = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
elif platform == "linux":
    not_allowed = ['/', '"', '\'', " "]

def mac_engine(_text, _voice, _rate, _path):
    subprocess.call(["say", _text, "-o", _path, f"--rate={_rate}", "-v", _voice])

def engine(_text, _voice, _rate, _path):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[int(_voice)].id)
    engine.setProperty('rate', int(_rate))
    engine.save_to_file(_text, _path)
    engine.runAndWait()

def sanitize_filename(s):
    # binary search to limit filename to max_bytes
    low, high = 0, len(s)
    while low < high:
        mid = (low + high + 1) // 2
        if len(s[:mid].encode('utf-8')) <= max_bytes:
            low = mid
        else:
            high = mid - 1
    s = s[:low]

    # remove special characters based on platform
    s = "".join([char for char in s if char not in not_allowed])

    # remove any characters that could raise UnicodeEncodeError
    # as we gave the option to open files with any type of encoding
    s = s.encode('utf-8', 'ignore').decode('utf-8')

    # worst case filename will be a timestamp
    if not len(s): s = ""

    return f"{s}_{time.strftime('%H%M%S')}.aiff"

# TODO make these all keyword arguments, reduce length of name maybe new_strip i.e text_to_sound.new_strip()
def sound_strip_from_text(context, text, pitch, start_frame, voice, audio_channel, rate):
    relpath = False
    file_path = bpy.context.scene.render.filepath
    if (file_path[0:2] == "//"):
        relpath = True
        file_path = bpy.path.abspath(bpy.context.scene.render.filepath)

    b_ID = sanitize_filename(text)
    output_file = os.path.join(file_path, b_ID)

    if platform == "darwin":
        mac_engine(text, voice, rate, output_file)
    else:
        engine(text, voice, rate, output_file)

    _scene = context.scene
    if not _scene.sequence_editor:
        _scene.sequence_editor_create()
    seq = _scene.sequence_editor

    if relpath:
        b_obj = seq.sequences.new_sound(b_ID, filepath=bpy.path.relpath(output_file), channel=audio_channel, frame_start=start_frame)
    else:
        b_obj = seq.sequences.new_sound(b_ID, output_file, channel=audio_channel, frame_start=start_frame)

    # set pitch for 3 different implementations (it's sounding amazing in 4.x.x)
    if bpy.app.version >= (4, 0, 0):
        bpy.ops.sequencer.select_all(action='DESELECT')
        b_obj.select = True
        bpy.context.scene.sequence_editor.active_strip = b_obj
        bpy.ops.sequencer.retiming_segment_speed_set(speed=pitch, keep_retiming=True)
    elif bpy.app.version >= (3, 3, 0):
        b_obj.speed_factor = pitch
    else:
        b_obj.pitch = pitch

    return b_obj, b_ID

def test_sanitize_filename():
    tests = [
        "This is a filename with English characters, and it is quite a bit longer than the previous one. In fact, it's so long that it might exceed\
        some file systems' filename length limits!This is a filename with English characters, and it is quite a bit longer than the previous one.\
        In fact, it's so long that it might exceed some file systems' filename length limits!",

        "这是一个包含中文字符的文件名，它比以前的文件名要长得多。实际上，它如此之长，可能超过某些文件系统的文件名长度限制\
        这是一个包含中文字符的文件名，它比以前的文件名要长得多。实际上，它如此之长，可能超过",

        "これは日本語の文字が含まれるファイル名であり、以前のものよりもはるかに長いです。実際、それは非常に長いため、一部のファイルシステムのファイル名の長さ制限を超える可能性があります\
            含まれるファイル名であり、以前のものよりもはるかに長いです。実際、それは非常に長いため、一部のファイルシステムのファイル名の長さ制限を超える可能性があります！",

        "이것은 한국어 문자가 포함 된 파일 이름이며 이전 것보다 훨씬 길다. 실제로 그것은 너무 길어서 일부 파일 시스템의 파일 이름 길이 제한을 초과할 수 있다!",

        "هذا هو اسم الملف الذي يحتوي على أحرف عربية، وهو أطول بكثير من السابق. في الواقع، فإنه طويل للغاية قد يتجاوز حد الأحرف المسموح به في بعض أنظمة الملفات!\
        هذا هو اسم الملف الذي يحتوي على أحرف عربية، وهو أطول بكثير من السابق. في الواقع، فإنه طويل للغاية هذا هو اسم الملف الذي يحتوي على أحرف عربية، وهو أطول بكثير من السابق. في الواقع، فإنه طويل للغاية ",

        "Это имя файла с русскими символами, и оно гораздо длиннее предыдущего. На самом деле, оно настолько длинное, что может превысить допустимую длину имени файла в некоторых файловых системах!\
        ми символами, и оно гораздо длиннее предыдущего. На самом деле, оно нми символами, и оно гораздо длиннее предыдущего. На самом деле, оно нми символами, и оно гораздо длиннее предыдущего. На самом деле, оно н\
        ми символами, и оно гораздо длиннее предыдущего. На самом деле, оно нми символами, и оно гораздо длиннее предыдущего. На самом деле, оно нми символами, и оно гораздо длиннее предыдущего. На самом деле, оно н\
        ми символами, и оно гораздо длиннее предыдущего. На самом деле, оно нми символами, и оно гораздо длиннее предыдущего. На самом деле, оно нми символами, и оно гораздо длиннее предыдущего. На самом деле, оно н\
        ми символами, и оно гораздо длиннее предыдущего. На самом деле, оно нми символами, и оно гораздо длиннее предыдущего. На самом деле, оно нми символами, и оно гораздо длиннее предыдущего. На самом деле, оно н",
    ]

    for test in tests:
       print(sanitize_filename(test))

if __name__ == "__main__":
    from timeit import timeit
    result = timeit(stmt=f"test_sanitize_filename()", globals=globals(), number=1)
    print(f"Execution time is {result / 1} seconds")
