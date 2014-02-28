#!/usr/bin/env python
import os
import sys
import zipfile

ext = os.path.splitext(os.environ['NZBNP_FILENAME'])[1]

if ext.lower() == '.zip':
    with zipfile.ZipFile(os.environ['NZBNP_FILENAME']) as zippedfile:
        zippedfile.extractall(os.environ['NZBNP_DIRECTORY'])
