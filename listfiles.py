import os
import sys

def main():
	if (not len(sys.argv) == 3):
		usage()
		exit(1)

	searchFiles(sys.argv[1], sys.argv[2])



def searchFiles(root, search):

	for root, dirs, files in os.walk(root):
		for file in files:
			if (search in file):
				print('{0:s}:'.format(root))
				print('    {0:s}'.format(file))

def usage():
	print('Usage: {0:s} <path> <search>'.format(sys.argv[0]))

if __name__ == '__main__':
    main()
