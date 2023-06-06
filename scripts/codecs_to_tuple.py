# to parse from table at https://docs.python.org/3/library/codecs.html

import sys
import os 
with open(os.path.join(sys.path[0], r"./codecs_raw")) as f:
    file = (f.read())

counter = 0
codec = []
alias = []
languages = []
for line in file.split('\n'):
    if line != '':
        if counter == 0:
            codec.append(line)
        if counter == 1:
            alias.append(line)
        if counter == 2:
            languages.append(line)
        counter += 1

        if counter == 3:
            counter = 0

for index, line in enumerate(codec):
    print(f"('{index}', '{line}', '{languages[index]} {alias[index]}'),")