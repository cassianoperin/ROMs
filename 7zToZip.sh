#!/bin/bash

# Variables
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
zip_extension="*.zip *.ZIP"
rom_extensions="*.z64 *.Z64"

# Colors
RED='\033[0;31m'
LIGHT_GREEN='\033[0;3s21m'
NC='\033[0m' # No Color

# Clean all previous roms
rm -rf $zip_extension $rom_extensions

echo -e "\nDecompressing files:\n"

# Extract all 7z files
for i in *.7z
do
   # Extract 7z roms
   7z e "$i" > /dev/null

   echo -ne "$i\033[0K\r"

done
echo -ne 'DONE\033[0K\r\n'

echo -e "\nCompressing files with ZIP:\n"

# Compress all .z64 files with zip
for i in *.z64
do
   tmp=$(echo $i |sed -e 's/.z64$//')
   zip -9 $tmp.zip $i > /dev/null

   echo -ne "$i\033[0K\r"
done
echo -ne 'DONE\033[0K\r\n'

# Clean uncompressed roms
rm -rf $zip_extension $rom_extensions

IFS=$SAVEIFS
