#!/usr/bin/python3
 
import sounddevice as sd
import soundfile as sf
import sys

def main():
	fileName = sys.argv[1]
	targetDevice = sys.argv[2]
	targetChannel = sys.argv[3]
	print (f"audioFile: {fileName} targetDevice:{targetDevice} targetChannel:{targetChannel} ")
	devicelist = sd.query_devices()
	print (f"attempt to play to :{devicelist[int(targetDevice)]['name']}")
	sd.default.device = devicelist[int(targetDevice)]["name"]
	for key in devicelist:
		print(key["name"])

	data, sr = sf.read(fileName)
	sd.play(data,sr,mapping=int(targetChannel))
	status = sd.wait()

def printUsage():
	print(f"Usage: playAudioToChannel <fileName> <device number> <target channel>")
	print("Devices:")
	print (sd.query_devices())

def checkArgs():
	if len(sys.argv) < 4:
		printUsage()
		return False
	
	return True

if __name__ == "__main__":
	print (f'args: {sys.argv}')
	if checkArgs() == False:
		exit()
	main()
