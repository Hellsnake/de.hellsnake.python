import sys
import visa
import time

def main():
	rm = visa.ResourceManager()
	checksum = ChecksumBuffer()
	command = str()
	response = ''	
	command_string_error = "RR,15;"

	resourceList = rm.list_resources()
	dev = rm.open_resource(resourceList[0])

	dev.encoding = 'cp437'
	#dev.chunksize = 10200;

	command = "DC;" + checksum.get("DC;") + "\n"
	#print("Sending command '{0:s}' to device".format(command))
	dev.write(command )
	response = dev.read()

	#while command_string_error in response:
	dev.write(command)
	time.sleep(4)
	response = dev.read()
	print("{0:s}".format(response))

	# command = "BW;" + checksum.get("BW;")
	# print("Sending command '{0:s}' to device".format(command))
	# dev.write(command)
	# response = dev.read()
	# print("{0:s}".format(response))

	dev.close()

	

	#print(checksum.get('BW;'))



class ChecksumBuffer:

	def __init__(self):
		self._listOfChecksums = {}
		self._offset = b'\x01\x00'

	def __add(self, value):
		bytelist = value.encode('cp437')

		# Summiere alle Dezimalwerte der Zeichen
		sum = 0;
		for b in bytelist:
			sum = sum + b
		#print(sum)
		

		# Offset als int (Hexadezimal = 100H) - errechnet Wert als int
		result = int.from_bytes(self._offset, byteorder = 'big') - sum.to_bytes(2, byteorder='big')[1]

		if result == 0:
			result = result + 256
		elif result == 10:
			result = result + 266

		#print(result)
		c = result.to_bytes(1, byteorder = 'big', signed=False)

		self._listOfChecksums[value] = c
		c = c.decode('cp437')

		return c
		
	def get(self, value):


		if value not in self._listOfChecksums.keys():
			print('Der Wert {0:s} ist noch nicht im Puffer'.format(value))
			return self.__add(value)

		return self._listOfChecksums[value]

if __name__ == '__main__':
    main()
