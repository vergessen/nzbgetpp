#!/usr/bin/env python
import os
import sys
import zipfile

ext = os.path.splitext(os.environ['NZBNP_FILENAME'])[1]
cat = os.environ['NZBNP_CATEGORY']
dir = os.environ['NZBNP_DIRECTORY']
filename = os.environ['NZBNP_FILENAME']
if ext.lower() == '.zip':
    zipf = zipfile.ZipFile(filename, mode='r')
    if cat != "":
        zipf.extractall(dir + os.path.sep + cat)
    else:
        zipf.extractall(dir)     

#file is there but has to be cleared on next pass?
#    os.unlink(os.environ['NZBNP_FILENAME'] + '.processed')
