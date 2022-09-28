import dir2csv

lib = r'C:\Program Files\Blender Foundation\Blender 3.3\3.3\python\lib'

## STEP 1, get file and folder list after custom libs are installed
#dir2csv.dir2csv(lib, "lib_custom")

## STEP 2, get file and folder list after fresh_install blender
#dir2csv.dir2csv(lib, "lib_fresh")

## STEP 3 compare to see what was downloaded
custom = dir2csv.csv2list("lib_custom")
fresh_install = dir2csv.csv2list("lib_fresh")

installed = []
for item in custom:
    if item not in fresh_install:
        installed.append(item)

# make csv of items to uninstall
dir2csv.list2csv(installed, "delete_list")

