import os
import platform
from datetime import datetime



def main():
	directory = 'F:/Log/'
	files = os.listdir(directory)
	stamps = 'stamps.txt'
	file_ending = '.blf'
	indexStart = 10
	indexEnd = 29
	header = "creationDate\t\t modificationDate\t substring\t\tFilesize\n"

	f = open(stamps, 'w')
	f.write(header)

	for file in files:	
		if os.path.isfile(directory + file):
			if file.endswith(file_ending):
				creationDate =  datetime.fromtimestamp(getCreationTime(directory + file)).strftime('%d.%m.%Y %H:%M:%S')
				modificationDate =  datetime.fromtimestamp(getModificationTime(directory + file)).strftime('%d.%m.%Y %H:%M:%S')
				size = getFileSize(directory + file)
				result = '|{0:s}|\t|{1:s}|\t|{2:s}|\t|{3:8.2f} KB|\n'.format(creationDate, modificationDate, file[indexStart:indexEnd],size / 1024 )
				f.write(result)
		else:
			print("{0} is not file".format(file))

	f.close()



def getCreationTime(path):

	if platform.system() == 'Windows':
		return os.path.getctime(path)

def getModificationTime(path):
	if platform.system() == 'Windows':
		return os.path.getmtime(path)

def getFileSize(path):
	if platform.system() == 'Windows':
		return os.path.getsize(path)


if __name__ == '__main__':
	main()