#!/usr/bin/python

import sys, os, shutil

libsource = 'lib/snemail.py'
binsource = 'bin/snemail'
libtarget = [f for f in sys.path if f.endswith('packages')][0] + '/' + 'snemail.py'
bintarget = "/usr/local/bin/" + 'snemail'

shutil.copy2(libsource, libtarget)
os.chmod(libtarget, 0755)
print '\nThe snemail libraries have been installed in ' + libtarget
shutil.copy2(binsource, bintarget)
os.chmod(bintarget, 0755)
print 'The snemail binary has been installed to ' + bintarget + '\n'
