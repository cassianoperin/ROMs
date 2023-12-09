#!/usr/bin/env python3

# Compress individually all roms in a folder
# for f in *; do zip -r "${f%%.*}.zip" "$f"; done

import os, shutil, re, sys

# Test number of arguments
if len(sys.argv) != 2 :
	print("Usage:\t%s ROMS_PATH\n" % (sys.argv[0]) )
	sys.exit()

# Variables
filename = []		# list used to store the filtered roms
filename_revision = []	# list used to keep just the last revision of the rom
rom_path = sys.argv[1]		# roms path
extension = ['zip']	# rom extension

folder_USA     = "# USA/"
folder_Japan   = "# Japan/"
folder_Europe  = "# Europe/"
folder_PDABS   = "# Proto Demo Alpha Beta Sample/"
folder_old     = "# Old Revisions/"
folder_Other   = "# Other Regions/"

filter = {	# Proto Demo Alpha Beta Sample
		'(Beta': folder_PDABS, '(Proto': folder_PDABS, 'Proto)': folder_PDABS, '(Alpha': folder_PDABS, '(Demo': folder_PDABS, '(Sample': folder_PDABS, 'Sample ROM)': folder_PDABS, \
		# Other Regions
		'(Europe)': folder_Europe, '(Japan)': folder_Japan, '(France)': folder_Other, '(Germany)': folder_Other,	'(Spain)': folder_Other, '(China)': folder_Other, '(Canada)': folder_Other, \
		'(Korea)': folder_Other, '(Sweden)': folder_Other, '(Hong Kong)': folder_Other, '(Australia)': folder_Other, '(Italy)': folder_Other, '(Netherlands)': folder_Other, \
		'(Denmark)': folder_Other, '(Taiwan)': folder_Other, '(Sachen)': folder_Other, '(Russia)': folder_Other, '(Mexico)': folder_Other, '(Asia)' : folder_Other,\
		'(USA, Asia)': folder_Other, '(Europe, Australia)': folder_Other, '(Japan, Europe)': folder_Other, '(Japan, Korea)': folder_Other, '(Argentina)': folder_Other,\
		'(Asia, Korea)': folder_Other, '(Japan, Europe, Korea)': folder_Other, '(Europe, Korea)': folder_Other, '(Europe, Asia)': folder_Other, '(Asia, Australia)': folder_Other, \
		# Special Releases / Bios / Enhancement Chips
		'(Wii)': folder_Other,   '(Arcade)': folder_Other, 'Virtual Console': folder_Other, 'Switch Online': folder_Other, '(Castlevania Anniversary Collection)': folder_Other, \
		'(Enhancement Chip)': folder_Other, '[BIOS]': folder_Other, '(GameCube)': folder_Other, '(GameCube Edition)': folder_Other, '(SDK Build)': folder_Other, '(LodgeNet)': folder_Other, \
		# Other languages
		'(De)': folder_Other, '(Fr)': folder_Other, '(Es)': folder_Other, '(Ja)': folder_Other, \
		# Unlicensed
		'(Unl)': folder_Other,
		# USA
		'.zip': folder_USA }


###################### Create folders ######################

print("\nExecuting:\n\n1. Creating directories:")

os.chdir(rom_path)

for folder in folder_USA, folder_PDABS, folder_Japan, folder_Europe, folder_old, folder_Other:
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

for key in filter:

	# Reset Variables
	filename = []

	# Filter roms
	for r,d,f in os.walk("."):
	    for file in f:
	       if file[-3:] in extension and key in file:
	            filename.append(file)
	    break

	# Move Files
	for f in filename:
	   src = f
	   dst = filter[key]+f
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

	# Search for that prefix in files
	for r,d,f in os.walk("."):
		for file in f:
			# if file starts with game string
			if file.startswith(game):
				filename_revision.append(file)

		# print(filename_revision)

	filename_revision = sorted(set(filename_revision))

	# From all games with this prefix, keep just the most recent and move other to Old Revision folder

	# Ex.: ['Track & Field II (USA).zip', 'Track & Field II (USA) (Rev 1).zip']
	if len(filename_revision) == 2:
		src = filename_revision[1]
		dst = "../"+folder_old+filename_revision[1]
		shutil.move(src,dst)

	# Ex.: ['Untouchables, The (USA) (Rev 1).zip', 'Untouchables, The (USA) (Rev 2).zip', 'Untouchables, The (USA).zip']
	if len(filename_revision) > 2:
		for i in range(0, len(filename_revision)):
			if i != len(filename_revision) -2:
				# Move all except the last but one
				src = filename_revision[i]
				dst = "../"+folder_old+filename_revision[i]
				shutil.move(src,dst)

print("\nDONE!\n")
