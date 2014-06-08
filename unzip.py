#!/usr/bin/env python
#
##############################################################################
### NZBGET SCAN SCRIPT                                          ###

# Unzips zipped nzbs.
#
# NOTE: This script requires Python to be installed on your system.

##############################################################################
### OPTIONS                                                                ###
#
# Delete zip after extraction (0, 1).
# Remove zip when done processing.  Helps if you upload a generic named zip.
#remove_zip=0
### NZBGET SCAN SCRIPT                                          ###
##############################################################################

import os
import sys
import zipfile

filename = os.environ['NZBNP_FILENAME']
ext = os.path.splitext(filename)[1]
cat = os.environ['NZBNP_CATEGORY']
dir = os.environ['NZBNP_DIRECTORY']

if ext.lower() == '.zip':
    zipf = zipfile.ZipFile(filename, mode='r')
    if cat != "":
        zipf.extractall(dir + os.path.sep + cat)
    else:
        zipf.extractall(dir)     
    if(os.environ['NZBPO_REMOVE_ZIP']):
        os.unlink(filename)
