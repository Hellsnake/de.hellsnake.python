import re


def main():
	line = '#FALSE#\n1\n0\n1\n0\n1\n1\n2\n"Z\:\\ARBEIT\\aktuelle\ Projekte\\Ronny\\rb\.radimation\\templates\\TSF-Templates\\REChamb\.doc"\n""\n3\n5\n8\n38\n1\n0\n1\n5\n2\n"Start Time"'
	search = r'^#FALSE#[a-zA-Z0-9\n\"\\\:\s\.\-]*\"Start Time\"$'
	searchObj = re.search(search, line, re.M|re.I)

	if searchObj:
		print('Found')


if __name__ == '__main__':
    main()
