#!"/usr/bin/python3"

import sys
import os 
with open(os.path.join(sys.path[0], r"./voices_linux")) as f:
    file = (f.read())

langs = file.split('<')
langs = langs[1:len(langs)]

for index, lang in enumerate(langs):
    l = lang.split('\n')#.split('=')
    voice = l[0].split('=')[1]
    gender = l[3].split('=')[1]
    if gender == 'None':
        gender = ''
    print(f"('{index}', '{voice.capitalize()} - {gender.capitalize()}', ''),")