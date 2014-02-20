#!/usr/bin/env python

##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###

# Join numbered split files after download
#
# NOTE: Requires python and has been tested on debian.  Please note
# on the second pass it will skip output as this is by design because we just
# want the pars to check out the record again.

### NZBGET POST-PROCESSING SCRIPT                                          ###
##############################################################################

import re
import os
import sys

# Exit codes used by NZBGet
POSTPROCESS_SUCCESS=93
POSTPROCESS_ERROR=94
POSTPROCESS_PAR2=92
POSTPROCESS_SKIPPED=95

if not os.environ.has_key('NZBOP_SCRIPTDIR'):
	print('*** NZBGet post-processing script ***')
	print('This script is supposed to be called from nzbget (11.0 or later).')
	sys.exit(POSTPROCESS_ERROR)


if os.path.exists(os.environ['NZBPP_FINALDIR']):
    print('[DETAIL] Finaldir was found.  Using %s as the dir' % os.environ['NZBPP_FINALDIR'])
    dir = os.environ['NZBPP_FINALDIR']
else:
    print('[DETAIL] Finaldir was not found. Using %s as the dir' % os.environ['NZBPP_DIRECTORY'])
    dir = os.environ['NZBPP_DIRECTORY']


sys.stdout.flush()


matcher = re.compile('\.[0-9]+$')
chunks = []
for dirpath, dirnames, filenames in os.walk(os.environ['NZBPP_DIRECTORY']):
    for file in filenames:
        fileExtension = os.path.splitext(file)[1]
        if matcher.match(fileExtension):
            chunks.append(file)
if not chunks:
    print('[INFO] No files found to join')
    sys.exit(POSTPROCESS_SKIPPED)
chunks.sort()
wdata = ''
newfile = open(dir + os.path.sep + os.path.splitext(chunks[0])[0],"ab")
i = 0
for f in chunks:
    i = i + 1
    print('[INFO] joining file %s' % (dir + os.path.sep + f))
    part = open(dir + os.path.sep + f, "rb")
    reading = True
    while reading:
        wdata = part.read(4096)
        if (len(wdata) > 0):
            newfile.write(wdata)
        else:
           reading = False
    part.close()
    print('[INFO] delete file %s' % f)
    os.unlink(dir + os.path.sep + f)

newfile.close()

if os.environ['NZBPP_PARSTATUS'] == '0':
    sys.exit(POSTPROCESS_PAR2)
else:
    sys.exit(POSTPROCESS_SUCCESS)

