
class Checksum:

	@staticmethod
	def getVDSChecksum(stringValue, encoding = 'cp437'):
		listOfbytes = stringValue.encode(encoding)
		sumOfBytes = int()
		offset = b'\x01\x00'
		result = int()
		byteCount = int()

		for b in listOfbytes:
			sumOfBytes = sumOfBytes + b

		byteCount = 1 if round(sumOfBytes.bit_length() / 8) == 0 else round(sumOfBytes.bit_length() / 8) + 1

		result = int.from_bytes(offset, byteorder='big', signed=False) - sumOfBytes.to_bytes(byteCount, byteorder="big")[1]

		print("Checksum::getVDSChecksum sumOfBytes: '{sum:d}' (Byte Anzahl: {byteCount:d}) and result {result:d} for value '{val:s}'".format(sum = sumOfBytes, byteCount = byteCount, result=result, val = stringValue))
		return result.to_bytes(2, byteorder="big").decode(encoding)


print(Checksum.getVDSChecksum("AA,CC,DD,BB,DD,F,FF;"))
