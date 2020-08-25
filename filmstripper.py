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

    brkck()

    try:
        print("Reading output filename...")
        outputFile = sys.argv[2]
        print(outputFile)
    except:
        print("ERROR: Output file argument invalid.")
        sys.exit()
else:
    input_folder = "input/"
    outputFile = "output/output.png"

if path.isfile(outputFile):
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
            while path.isfile(outputFile):
                index = outputFile.find(".")
                newName = outputFile[:index] + str(random.randint(0, 9)) + outputFile[index:]
                print("New output filename: "+newName)
                outputFile = newName
            name_conflict = False
        else:
            print("Please write O, C or U.")

brkck()

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

brkck()

# Parsing the input arguments
# And setting up basic variables

fileList = glob.glob(str(input_folder+"*.*"))
fileList.sort()
firstFile = fileList[0]
inputExtension = str(firstFile.partition(".")[1]+firstFile.partition(".")[2])
firstFile.partition(".")[2]

if inputExtension:
    print("Input file extension found: "+inputExtension)
else:
    print("ERROR: Input file extension not found.")
    sys.exit()

brkck()

outputExtension = str(outputFile.partition(".")[1]+outputFile.partition(".")[2])

if outputExtension:
    print("Output file extension found: "+outputExtension)
elif inputExtension == ".jpg":
    print("Output file extension not found, using input file type, .jpg")
else:
    print("Output file extension not found, defaulting to .png")


# Setting up filmstrip buffer

print("Loading first image... "+firstFile)
firstImage = Image.open(firstFile)
width = firstImage.width
FSwidth = width
height = firstImage.height
FSheight = height
colorspace = firstImage.mode
print("Image attributes:")
print("Width: "+str(width))
print("Height: "+str(height))
print("Colorspace: "+colorspace)

if horizontal_rendering:
    FSwidth = 0
    widthAdd = width
    heightAdd = 0
else:
    FSheight = 0
    heightAdd = height
    widthAdd = 0

print("Creating filmstrip buffer...")
filmstrip = Image.new(colorspace, (FSwidth, FSheight))
print("Width: "+str(filmstrip.width))
print("Height: "+str(filmstrip.height))
print("Colorspace: "+filmstrip.mode)


# Adding each image to filmstrip

for eachFile in fileList:
    print("Loading "+eachFile+"...")
    eachImage = Image.open(eachFile)

    # Checking files for compatabililty

    if inputExtension not in eachFile:
        print("ERROR: Filetype mismatch.")
        sys.exit()
    if horizontal_rendering and eachImage.height != FSheight:
        print("ERROR: Image height mismatch.")
        sys.exit()
    if not horizontal_rendering and eachImage.width != FSwidth:
        print("ERROR: Image width mismatch.")
        sys.exit()
    if eachImage.mode != filmstrip.mode:
        print("ERROR: Image colorspace mismatch")
    brkck()

    extendedStrip = filmstrip.crop(box=(0, 0, filmstrip.width+widthAdd, filmstrip.height+heightAdd))
    extendedStrip.paste(eachImage, (extendedStrip.width-width, extendedStrip.height-height))
    filmstrip = extendedStrip
    print(eachFile+" added to filmstrip.")

print("Exporting filmstrip to "+outputFile)
filmstrip.save(outputFile)
print("Filmstrip exported.")
