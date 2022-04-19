#!"/usr/bin/python3"
from babel import Locale
import sys
import os 
with open(os.path.join(sys.path[0], r"./voices_osx")) as f:
    file = (f.read())

langs = file.split('<')
langs = langs[1:len(langs)]

for index, lang in enumerate(langs):
    l = lang.split('\n')#.split('=')
    voice = l[0].split('=')[1].split('.')[5]
    gender = l[3].split('=')[1].split('VoiceGender')[1]
    code = l[2].split("'")[1]
    if code[2] == '_':
        locale = code.split('_')[0]
        territory = code.split('_')[1]
    else:
        locale = code.split('-')[0]
        territory = code.split('-')[1]
    try:
        locale = Locale(locale, territory)
        country = locale.display_name
    except:
        country = code
    #print(f"('{index}', '{voice.capitalize()} - {gender.capitalize()} - {country}', ''),")
    print(f"* {voice.capitalize()} - {gender.capitalize()} - {country.capitalize()}")