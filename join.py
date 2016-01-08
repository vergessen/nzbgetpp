#!/usr/bin/env python2

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


sys.stdout.flush()

matcher = re.compile('\.[0-9]+$')
chunks = []
chunks2 = []

for dirpath, dirnames, filenames in os.walk(os.environ['NZBPP_DIRECTORY']):
    for file in filenames:
        chunks.append(os.path.join(dirpath,file))

chunks2 = [f for f in chunks if matcher.search(f)]

if not chunks2:
    print('[DETAIL] No files found to join. Skipping join!')
    sys.exit(POSTPROCESS_SKIPPED)



sets = {}
set = None

for file in chunks2:
    start, finish = os.path.splitext(file)
    if start not in sets:
        sets[start] = []
    sets[start].append(file)

for set in sets:
    sets[set].sort()
    current = sets[set]
    outfile = set
    if os.path.isfile(outfile):
        if os.path.getsize(outfile) <= os.path.getsize(current[0]):
            if outfile + '.001' not in current:
                os.rename(outfile, outfile + '.001')
                current.append(outfile + '.001')
                current.sort()
            else:
                if os.environ['NZBPO_OVERWRITEFILES'] == 'yes':
                    os.unlink(outfile)
                else:
                    print('[ERROR] %s was found and does not match expected output size.  Not overwriting, OVERWRITEFILES is sent to %s' % (outfile, os.environ['NZBPO_OVERWRITEFILES']))
                    sys.exit(POSTPROCESS_ERROR)
        else:
            print('[DETAIL] %s was found at %s bytes. Output matches at %s bytes. Skipping join!' % (outfile, os.path.getsize(outfile),size))
            sys.exit(POSTPROCESS_SKIPPED)

    wdata = ''
    with open(outfile, "ab") as newfile:
        i = 0
        for f in current:
            i = i + 1
            print('[INFO] joining file %s' % f)
            with open(f, "rb") as part:
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
                os.unlink(f)
        newfile.close()
sys.exit(POSTPROCESS_SUCCESS)
