import csv
import os
import dir2csv
import shutil

lib = r'C:\Program Files\Blender Foundation\Blender 3.3\3.3\python\lib'

delete_list = dir2csv.csv2list("delete_list")

os.chdir(lib)

for item in delete_list:
    name = item[0].split('\'')[1]
    type = item[1].split('\'')[1]

    if type == 'file':
        if os.path.exists(name):
            os.remove(name)
            print("removed file " + name)
        else:
            print("didn't remove file " + name)

    if type == 'dir':
        if os.path.exists(name):
            shutil.rmtree(name)
            print("removed dir " + name)
        else:
            print("didn't remove dir " + name)