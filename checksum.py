
class Checksum:

	@staticmethod
	def getVDSChecksum(stringValue, encoding = 'cp437'):
		listOfbytes = stringValue.encode(encoding)
		sumOfBytes = int()
		offset = b'\x01\x00'
		result = int()

		for b in listOfbytes:
			sumOfBytes = sumOfBytes + b

		print("Checksum::getVDSChecksum sumOfBytes: '{sum:d}' ({bitCount:d}) for value '{val:s}'".format(sum = sumOfBytes, bitCount = sumOfBytes.bit_length(), val = stringValue))

		result = int.from_bytes(offset, byteorder='big', signed=False) - sumOfBytes
		print(result)


Checksum.getVDSChecksum("DC;")



