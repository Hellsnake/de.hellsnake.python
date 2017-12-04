import visa
import sys
sys.path.append('Z:/ARBEIT/aktuelle Projekte/Ronny/de.hellsnake.python/agilent/')
from visa_helper import PyVisa_Helper

INNCO_AM_SELECT = 0
INNCO_TTABLE_SELECT = 1
INNCO2000_COMMAND_DEVSELECT = "LD <DEVICE> DV"
INNCO2000_COMMAND_CURRENTPOS = "CP"
INNCO2000_COMMAND_NEXTPOS = "LD <POS> DG NP"
INNCO2000_COMMAND_START_NEXTPOS = "GO"
#def rotate_table(newPosition):


def main():
	dev = PyVisa_Helper.selectDevice();
	response = str()
	answer = str()
	
	
	dev.chunk_size = 10240
	dev.read_termination = "\n"
	dev.values_format.is_big_endian = False
	dev.write("*IDN?")
	response = dev.read()
	print("Gerät: {0:s}".format(response))
	dev.write(INNCO2000_COMMAND_DEVSELECT.replace("<DEVICE>", str(INNCO_TTABLE_SELECT)))
	response = dev.read()
	print("Geräteauswahl: {0:s}".format(response))


	while(answer != "b" or answer != "B"):
		dev.write(INNCO2000_COMMAND_CURRENTPOS)
		response = dev.read()
		
		answer = input("Neue Tischposition wählen (aktuelle Position {curPos:s}°, (B/b: Beenden)):".format(curPos=response))

		# NP ist das Register, worauf der GO-Befehl zurückgreift
		# Das stellt die neue Position dar, Angabe in DG (Degree)
		dev.write(INNCO2000_COMMAND_NEXTPOS.replace("<POS>", answer))
		response = dev.read()
		print("Nächste Position {0:s}°".format(response))

		dev.write(INNCO2000_COMMAND_START_NEXTPOS)
		response = dev.read()
		print("Nächste Position {0:s}°".format(response))


	dev.close()







if __name__ == '__main__':
    main()