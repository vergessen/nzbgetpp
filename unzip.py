#!/usr/bin/env python
import os
import sys
import zipfile

ext = os.path.splitext(os.environ['NZBNP_FILENAME'])[1]
cat = os.environ['NZBNP_CATEGORY']
if ext.lower() == '.zip':
    zipf = zipfile.ZipFile(os.environ['NZBNP_FILENAME'], mode='r')
    zips = zipf.infolist()
    for sf in zips:
         if cat != "":
             zipf.extract(sf,os.environ['NZBNP_DIRECTORY'] + os.path.sep + os.environ['NZBNP_CATEGORY'])
         else:
             zipf.extract(sf,os.environ['NZBNP_DIRECTORY'])

#file is there but has to be cleared on next pass?
#    os.unlink(os.environ['NZBNP_FILENAME'] + '.processed')
