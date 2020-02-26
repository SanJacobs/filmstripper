from PIL import Image
import glob
import sys

broke = False

def brkck(**args):
    forcer = None
    if args:
        forcer = args[0]
    if broke or forcer:
        sys.exit()
    else:
        None


# Reading the input arguments
try:
    print("Reading input folder...")
    inputFolder = sys.argv[1]
    print(inputFolder)
except:
    print("ERROR: Input folder argument invalid.")
    broke = True

brkck()

try:
    print("Reading output filename...")
    outputFile = sys.argv[2]
    print(outputFile)
except:
    print("ERROR: Output file argument invalid.")
    broke = True

brkck()

try:
    if "v" in sys.argv[3] or "V" in sys.argv[3]:
        print("Using vertical layout")
        horiz = False
    elif "h" in sys.argv[3] or "H" in sys.argv[3]:
        print("Using horizontal layout")
        horiz = True
    else:
        print(str('ERROR: "'+sys.argv[3])+'"'+" is not a recognized layout. Use H or V.")
        broke = True
except:
    horiz = False

brkck()

# Parsing the input arguments
# And setting up basic variables

fileList = glob.glob(str(inputFolder+"*.*"))
fileList.sort()
firstFile = fileList[0]
inputExtension = str(firstFile.partition(".")[1]+firstFile.partition(".")[2])
firstFile.partition(".")[2]

if inputExtension:
    print("Input file extension found: "+inputExtension)
else:
    print("ERROR: Input file extension not found.")
    broke = True

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

if horiz:
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
        broke = True
    if horiz and eachImage.height != FSheight:
        print("ERROR: Image height mismatch.")
        broke = True
    if not horiz and eachImage.width != FSwidth:
        print("ERROR: Image width mismatch.")
        broke = True
    if eachImage.mode != filmstrip.mode:
        print("ERROR: Image colorspace mismatch")
    brkck()
    
    extendedStrip = filmstrip.crop(box=(0, 0, filmstrip.width+widthAdd, filmstrip.height+heightAdd))
    extendedStrip.paste(eachImage, (extendedStrip.width-width, extendedStrip.height-height))
    filmstrip = extendedStrip


filmstrip.save(outputFile)
