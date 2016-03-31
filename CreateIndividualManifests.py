#!/usr/bin/python

##########
## Author aysiu, 2016
## Apache license
##########

#### This script is to be run on the server side.

import os
import plistlib
from shutil import copyfile
import sys

# Manifest subdirectory
manifest_subdir='manifests'
####
#### Populate the dictionary below with the actual new manifest names and corresponding old manifest names
####
# Define dictionary of old manifest names and new manifest names
manifest_translation={ "NEWNAME1" :  "OLDNAME1", "NEWNAME2" :  "OLDNAME2", "NEWNAME3" :  "OLDNAME3" }

def main():
	# Find the path to the Munki repository
	munkiimport_prefs_location=os.path.join(os.getenv("HOME"), "Library/Preferences/com.googlecode.munki.munkiimport.plist")
	if os.path.exists(munkiimport_prefs_location):
		munkiimport_prefs=plistlib.readPlist(munkiimport_prefs_location)
		MUNKI_ROOT_PATH=munkiimport_prefs['repo_path']
	else:
		print "Cannot determine the Munki repo path. Be sure to run /usr/local/munki/munkiimport --configure to set the path for your user."		
		sys.exit(1)

	# Variable for manifest path
	manifest_path=os.path.join(MUNKI_ROOT_PATH, manifest_subdir)
	# Check the path exists
	if not os.path.exists(manifest_path):
		print 'Manifest path %s does not exist' % manifest_path
		sys.exit(1)
	else:
		# Check the path is writable by the user running this script
		if not os.access(manifest_path, os.W_OK):
			print 'You do not have write access to the %s folder' % manifest_path
			sys.exit(1)
		else:
			print 'Using manifest path of %s' % manifest_path

	# Go through dictionary and process each key and value
	for new_man in manifest_translation:
		# Name old manifest
		old_man=manifest_translation[new_man]

		# Get full path to old manifest
		old_man_location=os.path.join(manifest_path, old_man)
		if not os.path.exists(old_man_location):
			print '%s does not exist' % old_man_location
			sys.exit(1)
		
		# Get the file ownership of the old manifest
		# Based on code from http://stackoverflow.com/a/927890
		stat_info = os.stat(old_man_location)
		old_uid = stat_info.st_uid
		old_gid = stat_info.st_gid
			
		# Get the catalogs array from the old manifest
		old_manplist=plistlib.readPlist(old_man_location)
		old_catalogs=old_manplist['catalogs']

		# Create new dictionary based on old catalogs and old name
		# Based on code from Munki's manifestutil
		manifest_dict = {'catalogs': old_catalogs,
                'included_manifests': [old_man],
                'managed_installs': [],
                'managed_uninstalls': []}
		new_manifest_path = os.path.join(manifest_path, new_man)
		if os.path.exists(new_manifest_path):
			print '%s already exists!' % new_man
		else:
			print 'Creating %s to include %s with catalog(s) %s' % (new_man, old_man, old_catalogs)
			plistlib.writePlist(manifest_dict, new_manifest_path)
			# Make sure the ownership matches the old manifest
			os.chown(new_manifest_path, old_uid, old_gid)

if __name__ == '__main__':
   main()
