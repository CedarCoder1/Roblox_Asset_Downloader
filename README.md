# Roblox Asset Downloader
Lets users download all of the Roblox client and studio stuff from the setup cdn website. Also automatically puts the files in the right place. Written in Python.

The output and extra's folders contain parts of an example downloaded build.
Currently supported builds:
* Roblox Player for Windows
* Roblox Studio for Windows
* RCC Service

Keep in mind this program also downloads files who's name start with a dot (.) and with "keepme", which are removed by the official Roblox installers on install or by the client on launch.

This program also downloads version specific files that aren't normally downloaded from the CDN servers. These files are put in a separate "Extra's" folder.

# Mass Edition
The mass edition python script found in this repository is a modifed version of the Roblox Asset Downloader made for bulk downloading version files. The script reads the bulk download list from a file called 'versionsToDownload.txt'. Example files for both the API version format and the 'normal' version format can be found under the 'mass edition examples' folder in this repository.

## Todo
* Correct file structure for MacOS.
* Make the Extra downloads feature, so all other stuff from the cdn can be downloaded easily.
* Check if the extra's folder contains ALL extra's.
* Archive.org support.
