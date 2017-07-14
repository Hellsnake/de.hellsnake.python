import sys
import visa
import time

def main():
	tries = 1
	stdout = sys.stdout
	rm = visa.ResourceManager()
	resourceList = rm.list_resources()
	dev = rm.open_resource(resourceList[0], send_end=True, query_delay = 1.0)
	checksum = ChecksumBuffer()
	command = "DC;"
	response = ''	
	cs = checksum.get(command)
	command = command + cs + "\n"


	dev.encoding = 'cp437'

	print("{0:s}".format(command))
	response = dev.query(command)

	while "VDS" not in response and tries <= 10:
		dev.write(command)
		response = dev.read()
		stdout.write("Versuch {0:d}, Response: {1:s}\r".format(tries, response))
		stdout.flush()
		tries = tries + 1
		time.sleep(2)

	print(response)

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
