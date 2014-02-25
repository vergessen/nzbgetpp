#!/usr/bin/env python

##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###

# Join numbered split files after download
#
#
# This script joins *.001 etc files
#
#
# NOTE: Requires python
#
#
# Please note on the second pass it will skip output as this is by design because we just
# want the pars to check out the record again.

##############################################################################
### OPTIONS                                                                ###
# Preserve orginal files (yes, no).
#
#Preservefiles=no
#
# Overwrite output file (yes, no).
#
#
# In the case that both *.001 and the output file exists but is not the
# expected size should the output file be overwritten.
#
#Overwritefiles=yes
#
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
#    print('[INFO] Finaldir was found.  Using %s as the dir' % os.environ['NZBPP_FINALDIR'])
    dir = os.environ['NZBPP_FINALDIR']
else:
#    print('[INFO] Finaldir was not found. Using %s as the dir' % os.environ['NZBPP_DIRECTORY'])
    dir = os.environ['NZBPP_DIRECTORY']


sys.stdout.flush()


matcher = re.compile('\.[0-9]+$')
chunks = []
size = 0

for dirpath, dirnames, filenames in os.walk(os.environ['NZBPP_DIRECTORY']):
    for file in filenames:
        fileExtension = os.path.splitext(file)[1]
        if matcher.match(fileExtension):
            chunks.append(file)
            size = size + os.path.getsize(os.path.join(dir,file))

if not chunks:
    print('[DETAIL] No files found to join')
    sys.exit(POSTPROCESS_SKIPPED)

chunks.sort()
outfile = os.path.join(dir,os.path.splitext(chunks[0])[0])
if os.path.isfile(outfile):
    if os.path.getsize(outfile) != size:
        if os.path.splitext(chunks[0])[0] + '.001' not in chunks:
            os.rename(outfile, outfile + '.001')
            chunks.append(os.path.splitext(chunks[0])[0] + '.001')
            chunks.sort()
        else:
            if os.environ['NZBPO_OVERWRITEFILES'] == 'yes':
                os.unlink(outfile)
            else:
                print('[ERROR] %s was found and does not match expected output size.  Not removing outfile.' % outfile)
                sys.exit(POSTPROCESS_ERROR)
            
    else:
        print('[DETAIL] %s was found and matches the expected output size from the join procedure.  Skipping join!' % outfile)
        sys.exit(POSTPROCESS_SKIPPED)
     
wdata = ''
newfile = open(outfile, "ab")
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
    if os.environ['NZBPO_PRESERVEFILES'] == 'yes':
        print ('[INFO] File %s was not deleted' % f)
    else:
        print('[INFO] deleted file %s' % f)
        os.unlink(dir + os.path.sep + f)

newfile.close()

if os.environ['NZBPP_PARSTATUS'] == '0':
    sys.exit(POSTPROCESS_PAR2)
else:
    sys.exit(POSTPROCESS_SUCCESS)
