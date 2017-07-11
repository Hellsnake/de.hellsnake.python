import sys

def main():
	checksum = ChecksumBuffer()

	print(checksum.get('DE,15;'))



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

		# Offset als int (Hexadezimal = 100H) - errechnet Wert als int
		result = int.from_bytes(self._offset, byteorder = 'big') - sum.to_bytes(2, byteorder='big')[1]
		c = result.to_bytes(1, byteorder = 'big', signed=False)

		self._listOfChecksums[value] = c
	
		return c
		
	def get(self, value):


		if value not in self._listOfChecksums.keys():
			print('Der Wert {0:s} ist noch nicht im Puffer'.format(value))
			return self.__add(value)

		return self._listOfChecksums[value]

if __name__ == '__main__':
    main()