#!/usr/bin/python

import sys, os, shutil
import argparse

parser = argparse.ArgumentParser(description='sneMail install script', prog='install.py', version='0.1', usage='%(prog)s [-h] [-v]',
	epilog='Also refer to the README file for more info')
action = parser.add_mutually_exclusive_group(required=False)
action.add_argument('--install', action='store_true', help='will install all the files in the correct place')
action.add_argument('--uninstall', action='store_true', help='tries to remove all files that were installed')
action.add_argument('--update', action='store_true', help='same as --install, but skips installation of mysql-template')
parser.add_argument('--prefix', type=str, default='/usr/local/', help='Defaults to /usr/local/')
parser.add_argument('--os', type=str, default='centos', help='Defaults to centos, ubuntu/debian will be available soon')
args = parser.parse_args()

def snemail_packaging(os):
	print os

def snemail_install(prefix):
	libsource = 'lib/snemail.py'
	binsource = 'bin/snemail'
	etcsource = 'etc/snemail.conf'
	libtarget = [f for f in sys.path if f.endswith('packages')][0] + '/' + 'snemail.py'
	bintarget = prefix + 'bin/snemail'
	etctarget = '/etc/snemail.conf'
	
	shutil.copy2(libsource, libtarget)
	os.chmod(libtarget, 0700)
	print '\nThe snemail libraries have been installed in ' + libtarget
	shutil.copy2(binsource, bintarget)
	os.chmod(bintarget, 0700)
	print 'The snemail binary has been installed to ' + bintarget
	shutil.copy2(etcsource, etctarget)
	os.chmod(etctarget, 0700)
	print 'The snemail config has been installed to' + etctarget + '\n'
	print 'Continuing with packages: \n'
	if args.os == 'ubuntu' or args.os == 'debian':
		print 'Debian & Ubuntu are not supported yet, exiting now.' 
		sys.exit(0)
	elif args.os == 'centos':
		snemail_packaging(args.os) 

def snemail_uninstall():
	print 'uninstall function'

def snemail_update():
	print 'update function'

if len(sys.argv) == 1:
	parser.print_help()
	sys.exit(0)
if args.install is True:
	snemail_install(args.prefix)
