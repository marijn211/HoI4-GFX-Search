#created by marijn211

import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH) #navigate to location of this codefile
savegoal = ROOT_PATH + "\converted"
if not os.path.exists(savegoal):
  os.mkdir(savegoal)
  
if os.path.exists(savegoal + "\convertedfiles.txt"):
	with open(savegoal + "\convertedfiles.txt") as f:
		lines = f.read().splitlines()
else:
	lines = list()

defaultdlc = "dlc-base"

template = """
        <div data-clipboard-text="@GFX_token" data-search-text="@GFX_token" title="@GFX_token" class="icon @DLC">
            <img loading="lazy" src="@GFXPATH" alt="@GFX_token">
        </div>
"""

def removecomment(lineinput):            #if text to parse comes *after* a comment, then ignore it
	lineinput = lineinput.split("#")
	return lineinput[0]

filelist = os.listdir()
finallist = list()
for file in filelist:
	if (file not in lines) and (os.path.isfile(file)) and (file.split(".")[-1] == "gfx"):
		finallist.append(file)
	else:
		print("Skipping file {}".format(file))

for file in finallist:
	filenameelements = file.split('.')						#using [0] causes issues for filenames with dots
	filename = '.'.join(filenameelements[:-1]) + ".txt"

	DLC = input("Please enter what string value to use for DLC in {}, these tokens all start with dlc-, if you are entering focus icons, simply press enter\n".format(filename))
	if DLC == "":
		DLC = defaultdlc

	with open( file, encoding='utf-8' ) as fp:
		currtext = fp.read()

	currtext = currtext.replace(" ", "")						#remove spaces
	currtext = currtext.replace("\t", "")						#remove spaces
	currtext = currtext.split("\n")								#split lines, only necessary for next step
	currtext = "".join([removecomment(x) for x in currtext])	#discard any code behind comments, put the text back together
	currtext = currtext.replace("\n", "")						#discard newline symbols
	gfxtables = currtext.split("SpriteType={")

	os.chdir(savegoal)

	for table in gfxtables:
		outputtext = template

		elements = table.split("\"")
		checktype = None

		for element in elements:
			if checktype == "GFX_token":
				outputtext = outputtext.replace("@GFX_token", element)
				checktype = None
			elif checktype == "GFX_path":
				element = element.replace(".dds", ".png")
				outputtext = outputtext.replace("@GFXPATH", element)
				checktype = None
			elif "name" in element:
				checktype = "GFX_token"
			elif "texturefile" in element.lower():
				checktype = "GFX_path"

		outputtext = outputtext.replace("@DLC", DLC)
		if "@" not in outputtext:
			with open(filename, "a") as output:
				output.write(outputtext)
	with open("convertedfiles.txt", "a") as logfile:
		logfile.write(file+"\n")
	print("Successfully converted file {}".format(file))
	os.chdir(ROOT_PATH)
print("Finished conversion")
input("Press Enter to exit...")
