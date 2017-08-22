import sys
import visa
import time

# Klasse für die Response-Codes für den VDS
class VDSResponse:
	RESPONSE_SUCCESS = 'RR,00;\n'
	RESPONSE_READY_SINGLE_EVENT = 'RR,02;\n'
	RESPONSE_FAIL1 = 'RR,05;\n'
	RESPONSE_FAIL2 = 'RR,06;\n'
	RESPONSE_CONT_AFTERFAIL2 = 'RR,07;\n'
	RESPONSE_OVERCURRENT = 'RR,08\n'
	RESPONSE_CONT_AFTEROVERCURRENT = 'RR,09\n'
	RESPONSE_ERR_TRANSMIT = 'RR,10\n'
	RESPONSE_ERR_TEST_ON = 'RR,11;\n'
	RESPONSE_ERR_VALUE_LIMIT = 'RR,14;\n'
	RESPONSE_ERR_CHECKSUM = 'RR,15;\n'
	RESPONSE_ERR_OVERVOLTAGE_TEMP_DCSRC = 'RR,17;\n'
	RESPONSE_ERR_NOTCORRECTABLE_LIMITATION = 'RR,20;\n'
	


def main():
	rm = visa.ResourceManager()
	checksum = ChecksumBuffer()
	command = str()
	response = ''	
	err_checksum = 'RR,15;\n'
	err_test_on = 'RR,11;\n'
	device_gpibid = 'GPIB0::14::INSTR'
	set_supply_command = 'UR,<Ub>,<I>,<modUR>;'

	resourceList = rm.list_resources()

	if device_gpibid not in resourceList:
		print("Teilnehmer {0:s} wurde nicht am GPIB gefunden. Beende Programm.".format(device_gpibid))
		exit(1)

	dev = rm.open_resource(device_gpibid)

	dev.encoding = 'cp437'
	# dev.read_termination = '\n'
	
	# Wichtig!!! Standardmäßig auf CR gesetzt ('\r'), benötigt dann kein '\n' mehr
	# beim command
	dev.write_termination = '\n'
	dev.send_end = False
	#dev.chunksize = 10200;
	
	command = 'DC;' + checksum.get('DC;')
	print("Schreibe {0:s} zum Gerät {1:s} ".format(command, device_gpibid))
	dev.write(command)
	dev.wait_for_srq()
	response = dev.read()
	print("Gerät meldet sich mit: {0:s}".format(response))


	command = 'BS,1;' + checksum.get('BS,1;')
	print("Schreibe {0:s} zum Gerät {1:s} ".format(command, device_gpibid))
	dev.write(command)
	dev.wait_for_srq()
	response = dev.read()
	print("Gerät meldet sich mit: {0:s}".format(response))

	ub = int(float(input("Gewünschte Spannung eingeben (in V):")) * 10)
	imax = int(input("Strombegrenzung eingeben(in A):"))
	command = set_supply_command.replace("<Ub>",str(ub))
	command = command.replace("<I>", str(imax))
	command = command.replace("<modUR>", str(2))


	command = command + checksum.get(command)
	print("Schreibe {0:s} zum Gerät {1:s} ".format(command, device_gpibid))
	dev.write(command)
	dev.wait_for_srq()
	response = dev.read()
	print("Gerät meldet sich mit: {0:s}".format(response))
	if response == VDSResponse.RESPONSE_ERR_TEST_ON:
		print('"Test On" ist nicht gedrückt!"')
	time.sleep(60)
	dev.close()

	

	#print(checksum.get('BW;'))



class ChecksumBuffer:

	def __init__(self):
		self._listOfChecksums = {}
		self._offset = b'\x01\x00'

	def _add(self, value):
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
			#print('Der Wert {0:s} ist noch nicht im Puffer'.format(value))
			return self.__add(value)

		return self._listOfChecksums[value]

if __name__ == '__main__':
    main()
