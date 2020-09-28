#!/usr/bin/env python3

import os, shutil, re

# Variables
filename = []			# empty list used to store the filtered roms
filename_revision = []
rom_path = "."			# roms path
extension = ['zip']		# rom extension

folder_USA     = "# USA/"
folder_PDABS   = "# Proto Demo Alpha Beta Sample/"
folder_Other   = "# Other Regions and Old Revisions/"

filters = [ '(Beta'     , '(Proto'    , 'Proto)'    , '(Alpha'    , '(Demo'     , \
			'(Sample'   , 'Sample ROM)', '(Europe'   , 'Europe)'   , '(USA'    , 'USA)'    , '.zip' ]
folders = [ folder_PDABS, folder_PDABS, folder_PDABS, folder_PDABS, folder_PDABS, \
			folder_PDABS, folder_PDABS , folder_Other, folder_Other, folder_USA, folder_USA, folder_Other ]


###################### Create folders ######################

print("\nExecuting:\n\n1. Creating directories:")

for folder in folder_USA, folder_PDABS, folder_Other:
	# Create Folders
	try:
	    os.mkdir(folder)
	except OSError:
		# pass
	    print ("\tDirectory " + '"' + "%s" % folder + '"' + " already exists.")
	else:
	    print ("\tSuccessfully created the directory " + '"' + "%s" % folder + '"')

################### Filter and Move ROMs ###################

print("\n2. Filtering ROMs:\n\tProto Demo Alpha Beta Sample\n\tOther Regions\n\tUSA")

for count in range(12):

	# Reset Variables
	filename = []

	# Filter roms
	for r,d,f in os.walk(rom_path):
	    for file in f:
	       if file[-3:] in extension and filters[count] in file:
	            filename.append(file)
	    break

	# Move Files
	for f in filename:
	   src = f
	   dst = folders[count]+f
	   shutil.move(src,dst)

##################### Revision Control #####################

print("\n3. Revision Control:\n\tMoving old revisions")

# Change working directory
os.chdir(folder_USA)

# Reset Variables
filename = []

# Filter roms
for r,d,f in os.walk("."):
	for file in f:
		if file[-3:] in extension and '(Rev ' in file:
			result = re.split(' \(Rev', file)
			# print(result)
			filename.append(result[0])
	filename = sorted(set(filename))

# List of games with revision, sorted and unique
for game in filename:
	# Reset Variables
	filename_revision = []

	# print("\nOriginal: "+game)

	# Search for that prefix in files
	for r,d,f in os.walk("."):
		for file in f:
			if game in file:
				filename_revision.append(file)
	filename_revision = sorted(set(filename_revision))
	# print(filename_revision)

	# From all games with this prefix, keep just the most recent and move other to Old Revision folder
	for i in range(0, len(filename_revision)):
		# print(filename_revision[i])
		if i > 0:
			src = filename_revision[i]
			dst = "../"+folder_Other+filename_revision[i]
			shutil.move(src,dst)

print("\nDONE!\n")
