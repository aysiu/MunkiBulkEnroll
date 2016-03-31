# MunkiBulkEnroll
Two scripts (server and client) that bulk create individual [Munki](https://github.com/munki/munki) manifests that include group manifests

## What does MBE do?
On the server side, it takes a dictionary (key/value) of old manifest names and new manifest names, and then it creates new manifests from the new manifest names with the old manifest as an included manifest.

On the client side, it takes a dictionary (key/value) of new manifest names and serial numbers, and then it changes the client identifier to be the new manifest name.

This then allows users to have a general manifest that can affect all users in a particular group (e.g., faculty at a school) while also allowing for more granular manifest changes on an individual level (e.g., a specific English or math teacher).

## Any caveats?
Lots. I didn't create these scripts for mass consumption or use, but others may still find them helpful, so you will likely want to tweak the scripts before using them.

* This is definitely not an out-of-the-box experience. You will have to populate Python dictionaries on both the server-side script and the client-side script. I generated them by doing a .csv export from [MunkiReport](https://github.com/munkireport/munkireport-php) and then doing a bit of sorting and data manipulation in both Excel and TextWrangler.
* There is very little error checking. I have some in there (like paths not existing). But the general assumption is that the admin using these scripts will look closely at her environment, and then tweak the script appropriately and run some tests before deploying it _en masse_. As an example, the server-side script will just create the new individual manifest. It won't check whether the new manifest already exists or not (and may get overwritten).
* The client-side script assumes that the client identifier is in /Library/Preferences/ManagedInstalls and not /var/root/Library/Preferences/ManagedInstalls. More details on [the Munki wiki](https://github.com/munki/munki/wiki/Preferences#secure-configuration) about the differences between the two.
* This should go without saying, but definitely test on a handful of clients before rolling out to all your Munki clients. If the script doesn't work and the Munki clients lose their connection to Munki, you'll have to [ARD](http://www.apple.com/remotedesktop/) or do something else to get the clients back on track to connecting to the Munki server.
* The server-side script tries to get the Munki repo location from a Mac OS X preference file, so if you're using Windows or Linux, you may want to hard-code the Munki repo location.
* Because I coudln't get plistlib to work reliably with /Library/Preferences/ManagedInstalls, I cheated a bit and threw in a bash (`defaults write`) command at the end of the client-side script. The rest is written in Python. On the server side, plistlib has worked fine for me to read the Munki repo location and to both read and write manifests. If you run into binary/XML issues reading from / writing to .plist files with plistlib, you may want to check out [FoundationPlist](https://github.com/munki/munki/blob/master/code/client/munkilib/FoundationPlist.py).

## How is this different from Munki Enroll?

There are at least two Munki Enroll forks I know about.

I believe [edingc's Munki Enroll](https://github.com/edingc/munki-enroll) is the original and basically has the clients check in with a .php file on the server and automatically create their own individual nested manifest.

[hunty1's fork of Munki Enroll](https://github.com/hunty1/munki-enroll) seems to create more of a folder-based hierarchy. I think it's based on Active Directory organizational units (not 100% sure on that).

The focus, in both cases, is on a fairly uniform automated system. Since my current school's install base is a bit quirky (no definite rule about basing the manifest name on the machine name, for example, or even easy rules based on laptop vs. desktop), I created these scripts to allow me to create individual manifests in _bulk_ while also having some measure of control over how the individual names are constructed.

If you're looking for a more automated (not just bulk) solution, definitely go with one of the Munki Enrolls!

## How do you use MBE?

* Download the two scripts.
* Populate (hopefully using spreadsheets or some other script, not just hand-typing) the dictionaries, replacing the placeholder ALLCAPS names with the actual names you want).
* Proofread the workflow of the scripts to make sure they fit your organization's needs.
* Run the server-side script first to make sure the new manifests get created.
* Create a .pkg or a nopkg from the client-side script and import that into Munki.
* Test it on a few clients (and make sure they can still connect to the Munki server after installing the .pkg or nopkg) before rolling out to your full install base.

## Are you maintaining this or taking feature requests or pull requests?
No. I have a few other projects I'm actively maintaining, but this one is totally a one-off. If people find it useful, great. If not, they can use Munki Enroll, or they can fork this project and try to make it more of a generic off-the-shelf experience.
