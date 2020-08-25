#!/usr/bin/env python3

from PIL import Image
import glob
import sys
import random
from os import path


# Reading the input arguments
if len(sys.argv) > 2:
    try:
        print("Reading input folder...")
        input_folder = sys.argv[1]
        print(input_folder)
    except:
        print("ERROR: Input folder argument invalid.")
        sys.exit()

    try:
        print("Reading output filename...")
        output_file = sys.argv[2]
        print(output_file)
    except:
        print("ERROR: Output file argument invalid.")
        sys.exit()
else:
    input_folder = "input/"
    output_file = "output/output.png"

if path.isfile(output_file):
    name_conflict = True
    while name_conflict:
        print("WARNING: Output file already exists. What would you like to do? Overwrite, Cancel or Unique?")
        answer = input("[O/C/U]: ")
        if answer == "O" or answer == "o":
            None
            name_conflict = False
        elif answer == "C" or answer == "c":
            sys.exit()
            name_conflict = False
        elif answer == "U" or answer == "u":
            while path.isfile(output_file):
                index = output_file.find(".")
                new_name = output_file[:index] + str(random.randint(0, 9)) + output_file[index:]
                print("New output filename: "+new_name)
                output_file = new_name
            name_conflict = False
        else:
            print("Please write O, C or U.")

try:
    if "v" in sys.argv[3] or "V" in sys.argv[3]:
        print("Using vertical layout")
        horizontal_rendering = False
    elif "h" in sys.argv[3] or "H" in sys.argv[3]:
        print("Using horizontal layout")
        horizontal_rendering = True
    else:
        print(str('ERROR: "'+sys.argv[3])+'"'+" is not a recognized layout. Use H or V.")
        sys.exit()
except:
    horizontal_rendering = False

# Parsing the input arguments
# And setting up basic variables

file_list = glob.glob(str(input_folder+"*.*"))
file_list.sort()
first_file = file_list[0]
input_extension = str(first_file.partition(".")[1]+first_file.partition(".")[2])
first_file.partition(".")[2]

if input_extension:
    print("Input file extension found: "+input_extension)
else:
    print("ERROR: Input file extension not found.")
    sys.exit()

output_extension = str(output_file.partition(".")[1]+output_file.partition(".")[2])

if output_extension:
    print("Output file extension found: "+output_extension)
elif input_extension == ".jpg":
    print("Output file extension not found, using input file type, .jpg")
else:
    print("Output file extension not found, defaulting to .png")


# Setting up filmstrip buffer

print("Loading first image... "+first_file)
first_image = Image.open(first_file)
width = first_image.width
fs_width = width
height = first_image.height
fs_height = height
colorspace = first_image.mode
print("Image attributes:")
print("Width: "+str(width))
print("Height: "+str(height))
print("Colorspace: "+colorspace)

if horizontal_rendering:
    fs_width = 0
    width_add = width
    height_add = 0
else:
    fs_height = 0
    height_add = height
    width_add = 0

print("Creating filmstrip buffer...")
filmstrip = Image.new(colorspace, (fs_width, fs_height))
print("Width: "+str(filmstrip.width))
print("Height: "+str(filmstrip.height))
print("Colorspace: "+filmstrip.mode)


# Adding each image to filmstrip

for each_file in file_list:
    print("Loading "+each_file+"...")
    each_image = Image.open(each_file)

    # Checking files for compatabililty

    if input_extension not in each_file:
        print("ERROR: Filetype mismatch.")
        sys.exit()
    if horizontal_rendering and each_image.height != fs_height:
        print("ERROR: Image height mismatch.")
        sys.exit()
    if not horizontal_rendering and each_image.width != fs_width:
        print("ERROR: Image width mismatch.")
        sys.exit()
    if each_image.mode != filmstrip.mode:
        print("ERROR: Image colorspace mismatch")

    extended_strip = filmstrip.crop(box=(0, 0, filmstrip.width+width_add, filmstrip.height+height_add))
    extended_strip.paste(each_image, (extended_strip.width-width, extended_strip.height-height))
    filmstrip = extended_strip
    print(each_file+" added to filmstrip.")

print("Exporting filmstrip to "+output_file)
filmstrip.save(output_file)
print("Filmstrip exported.")
