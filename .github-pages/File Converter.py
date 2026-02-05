#created by marijn211

from PIL import Image
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

errorcount = 0
filelist = os.listdir()
finallist = list()
for file in filelist:
	if (file not in lines) and (os.path.isfile(file)) and (file.split(".")[-1] != "py"):
		finallist.append(file)
	else:
		print("Skipping file {}".format(file))

for idx, file in enumerate(finallist):
	try:
		if ".gif" in file:
			raise Exception('GIF could not be converted.')
		img = Image.open(file)
		#filename = str(idx) + ".png"	#necessitates that already used image indexes are skipped, making index useless

		filenameelements = file.split('.')						#using [0] causes issues for filenames with dots
		filename = '.'.join(filenameelements[:-1]) + ".png"

		os.chdir(savegoal)
		img.save(filename)
		with open("convertedfiles.txt", "a") as logfile:
			logfile.write(file+"\n")
		print("Successfully converted file {}".format(file))
		os.chdir(ROOT_PATH)
	except:
		imagepath = ROOT_PATH + "\\" + file
		#print("Could not convert file {} , copying over instead.".format(file))
		#cmd = f'copy "{imagepath}" "{savegoal}"'
		print("Could not convert file {} , ignoring it.".format(file))
		os.system(cmd)
		errorcount += 1
print("Finished conversion, ", errorcount, "files skipped.")
input("Press Enter to exit...")