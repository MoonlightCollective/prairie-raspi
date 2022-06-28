import random
import time
import soundfile
import sys
from os import listdir, popen
from os.path import join, isfile
import subprocess

folderName = ""
device = 0
nChannels = 2
nClips = 8
overlapMin = 0.1
overlapMax = 0.4

def main():
	fileList = findFileNames()
	if len(fileList) < nClips:
		print ("Couldn't find enough clips in folder!")
		exit(1)

	print(f"All possible audio files:{fileList}")

	shuffleDexList = []
	for i in range (0,len(fileList)-1):
		shuffleDexList.append(i)
	
	random.shuffle(shuffleDexList)

	dex = 0
	for i in range(0,nClips):
		dex = shuffleDexList[i]
		sfi = soundfile.info(fileList[dex])
		duration = sfi.duration
		cDex = random.randrange(1,nChannels)
		cmdLine = f'./playAudioToChannel.py {fileList[dex]} {device} {cDex}'
		print(f'play {fileList[dex]}')
		subprocess.Popen(['./playAudioToChannel.py',f'{fileList[dex]}',f'{device}',f'{cDex}'])
		overlap = random.randrange(overlapMin,overlapMax)
		waitSecs = duration - (float(overlap) / 100 * duration)
		print(f'wait {waitSecs} out of {duration}')
		time.sleep(waitSecs)

	print ('main')

def findFileNames():
	allContents = listdir(folderName)
	wavFiles = []
	for f in allContents:
		if isfile(join(folderName,f)) and f.endswith('.wav'):
			wavFiles.append(join(folderName,f))
	return wavFiles

def printUsage():
	print ('Usage: playEchoEvent <Folder Name> <device> <# channels> <# clips> <overlap % min (0-1)> <overlap % max (0-1)>')

def checkArgs():
	if len(sys.argv) < 7:
		printUsage();
		return False

def echoArgs():
	print (f'Folder: {folderName}')
	print (f'Device: {device}')
	print (f'Channel Count: {nChannels}')
	print (f'Clip count: {nClips}')
	print (f'Overlap: {overlapMin} - {overlapMax}')

if __name__ == "__main__":
	if checkArgs() == False:
		exit(-1)

	# parse args
	folderName = sys.argv[1]
	device = int(sys.argv[2])
	nChannels = int(sys.argv[3])
	nClips = int(sys.argv[4])
	overlapMin = int(sys.argv[5])
	overlapMax = int(sys.argv[6])

	echoArgs()

	# do the thing.
	main()
	
