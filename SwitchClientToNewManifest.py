#!/usr/bin/python

##########
## Author aysiu, 2016
## Apache license
##########

#### This script is to be run on the client side--distribute as a .pkg or as a nopkg with an installcheck_script

import os
import subprocess

# Fix the manifest on the client

####
#### Populate the dictionary below with the actual new manifest names and corresponding old manifest names
####
# Define the mappings for the new manifests
new_manifests={ "NEWNAME1" : "SERIALNUMBER1", "NEWNAME2" : "SERIALNUMBER2", "NEWNAME3" : "SERIALNUMBER3" }

# Code for serial number based on http://apple.stackexchange.com/a/40244
this_mac=os.popen('/usr/sbin/system_profiler SPHardwareDataType | /usr/bin/awk \'/Serial/ {print $4}\'').read().strip()

if this_mac in new_manifests:

   # Create the command to write the new manifest for the client
   #cmdOne='/usr/bin/defaults write /private/var/root/Library/Preferences/ManagedInstalls ClientIdentifier "' + new_manifests[this_mac] + '"'
   #cmdTwo='/usr/bin/defaults delete /Library/Preferences/ManagedInstalls ClientIdentifier'
   
   #print cmdOne
   #print cmdTwo

   cmd='/usr/bin/defaults write /Library/Preferences/ManagedInstalls ClientIdentifier "' + new_manifests[this_mac] + '"'

   #print cmd

   # Actually run the commands
   #subprocess.call(cmdOne, shell=True)
   #subprocess.call(cmdTwo, shell=True)
   subprocess.call(cmd, shell=True)
