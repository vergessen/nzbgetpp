#!/usr/bin/env python
import os
import sys
import zipfile

ext = os.path.splitext(os.environ['NZBNP_FILENAME'])[1]

if ext.lower() == '.zip':
    zipf = zipfile.ZipFile(os.environ['NZBNP_FILENAME'], mode='r')
    zips = zipf.infolist()
    for sf in zips:
         sf.filename = 'cat.'+ os.environ['NZBNP_CATEGORY'] + '.' + sf.filename
         zipf.extract(sf,os.environ['NZBNP_DIRECTORY'])
else:
    checkcat = os.environ['NZBNP_NZBNAME'].split('.',2)
    if checkcat[0] == 'cat':
       print("[NZB] NZBNAME=%s" % checkcat[2])
       print("[NZB] CATEGORY=%s" % checkcat[1])
