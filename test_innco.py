import visa

INNCO_AM_SELECT = 0
INNCO_TTABLE_SELECT = 1
#def rotate_table(newPosition):


def main():
	rm = visa.ResourceManager()
	dev = rm.open_resource(rm.list_resources()[4])
	response = str()

	dev.chunk_size = 10240
	dev.read_termination = "\n"
	dev.values_format.is_big_endian = False
	dev.write("*IDN?")
	response = dev.read()
	print("Gerät: {0:s}".format(response))
	dev.write("LD command DV".replace("command", INNCO_TTABLE_SELECT))
	response = dev.read()
	print("Geräteauswahl: {0:s}".format(response))

	dev.write("CP")
	response = dev.read()
	print("Aktuelle Position {0:s}°".format(response))

	# NP ist das Register, worauf der GO-Befehl zurückgreift
	# Das stellt die neue Position dar, Angabe in DG (Degree)
	dev.write("LD 0 DG NP")
	response = dev.read()
	print("Nächste Position {0:s}°".format(response))

	dev.write("GO")
	response = dev.read()
	print("Nächste Position {0:s}°".format(response))


	dev.close()







if __name__ == '__main__':
    main()