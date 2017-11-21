import sys
import visa
import time


def main():
	rm = visa.ResourceManager()
	checksum = ChecksumBuffer()
	command = str()
	response = ''	
	err_checksum = 'RR,15;\n'
	err_test_on = 'RR,11;\n'
	device_resourceid = 'GPIB0::14::INSTR'
	set_supply_command = 'UR,<Ub>,<I>,<modUR>;'
	set_starttest_command = 'AA;'
	res_class = str()

	resourceList = rm.list_resources()

	if device_resourceid not in resourceList:
		print("Teilnehmer {0:s} wurde nicht am GPIB gefunden.".format(device_resourceid))
		device_resourceid = VisaHelper.selectResource()
		#if(not device_resourceid):
			#exit(1)

	dev = rm.open_resource(device_resourceid)
	# Resourcennamen für GPIB oder Serial
	res_class = type(dev).__name__

	dev.encoding = 'cp437'
	# dev.read_termination = '\n'
	
	# Wichtig!!! Standardmäßig auf CR gesetzt ('\r'), benötigt dann kein '\n' mehr
	# beim command
	dev.write_termination = '\n'
	dev.send_end = False
	#dev.query_delay = 3000
	#dev.chunksize = 10200;
	
	command = 'DC;' + checksum.get('DC;')
	dev.write(command)
	if res_class == 'GPIBInstrument':
		dev.wait_for_srq()
	response = dev.read()
	print("Request an {dev:20} Response".format(dev=device_resourceid))
	print("{req:31} {res:50}".format(req=command, res=response.replace('\n','')))


	command = 'BS,1;' + checksum.get('BS,1;')
	dev.write(command)
	if res_class == 'GPIBInstrument':
		dev.wait_for_srq()
	else:
		time.sleep(2.5)
	response = dev.read()
	print("{req:31} {res:50}".format(req=command, res=response.replace('\n','')))

	ub = int(float(input("Gewünschte Spannung eingeben (in V):")) * 10)
	imax = int(input("Strombegrenzung eingeben(in A):"))
	command = set_supply_command.replace("<Ub>",str(ub))
	command = command.replace("<I>", str(imax))
	command = command.replace("<modUR>", str(2))


	command = command + checksum.get(command)
	dev.write(command)
	if res_class == 'GPIBInstrument':
		dev.wait_for_srq()
	else:
		time.sleep(2.5)
	response = dev.read()
	while response == VDSResponse.RESPONSE_ERR_TEST_ON:
		inp = str()
		inp = input('"Test On" ist nicht gedrückt!"')
		dev.write(command)
		if res_class == 'GPIBInstrument':
			dev.wait_for_srq()
		else:
			time.sleep(2.5)
		response = dev.read()
	print("Request an {dev:20} Response".format(dev=device_resourceid))
	print("{req:31} {res:50}".format(req=command, res=response.replace('\n','')))


	# nextFunction = impulseSelection()

	# command = nextFunction()
	# command = command + checksum.get(command) + set_starttest_command + checksum.get(set_starttest_command)
	# dev.write(command)
	# if res_class == 'GPIBInstrument':
	# 	dev.wait_for_srq()
	# else:
	# 	time.sleep(2.5)
	# response = dev.read()
	# print("{req:31} {res:50}".format(req=command, res=response.replace('\n','')))

	# command = set_starttest_command + checksum.get(set_starttest_command)
	# dev.write(command)
	# if res_class == 'GPIBInstrument':
	# 	dev.wait_for_srq()
	# else:
	# 	time.sleep(2.5)
	# response = dev.read()
	# print("{req:31} {res:50}".format(req=command, res=response.replace('\n','')))


	inp = input("Enter drücken zum Beenden!")

	dev.close()



	""" 
	Gibt den Befehlsstring zurück für einen Impuls 2b
	Substitutionsstring: 'DA,Ub,Ua1,t1,t6,td,Int,n,tri,I,tdstep,tdstop;'
	Ub = Betriebsspannung (immer mit mal 10, Bsp: 13.5 V = 135)
	Ua1 = (Vmax - Ub) + Us (Bsp: 600 - 135 + 100 = 565)
	t1 = Zeit bis zum ersten Einbruch (0.1 s - 99.9 s, Bsp.: t1 = 1 = 0.1s, Zeit(in s) = Wert * 10 = 30)
	t6 = Zeit bis zum Impuls (1 ms - 999 ms, t6 = 1 = 1 ms)
	td = Pulsbreite des Impulses (5 ms - 9999 ms, td = 5 = 5 ms)
	Int = Intervall (0.1 - 99.9 s, Int = 1  = 0.1 s)
	n = Anzahl Impulse (1 - 30000)
	tri = Trigger (manuell(1) oder automatisch(0))
	I = Strombegrenzung
	"""
def getImpulse_2b(parameters = {'Ub':135, 'Ua1':565, 't1':1, 't6':1, 'td':2000, 'Int':1, 'n':10, 'tri': 0, 'I':10, 'step':2000, 'stop':2000}):
	set_impulse2b_command = 'DA,Ub,Ua1,t1,t6,td,Int,n,tri,I,step,stop;'
	command = str()

	for key in parameters:
		set_impulse2b_command = set_impulse2b_command.replace(key, str(parameters[key]))

	return set_impulse2b_command


	""" 
	Gibt den Befehlsstring zurück für einen Impuls 2b
	Substitutionsstring: 'DI,Ub,Ua1,Ua2,t1,t7,t8,,t9,t11,Ua,tri,I,n,5;'

	"""
# def getImpulse_4(parameters = {'Ub':135, 'Ua1':565, ,'Ua2':}):
# 	set_impulse_4_command = 'DI,Ub,Ua1,Ua2,t1,t7,t8,,t9,t11,Ua,tri,I,n,5;'
# 	command = str()

# 	for key in parameters:
# 		set_impulse2b_command = set_impulse2b_command.replace(key, str(parameters[key]))

# 	return (set_impulse2b_command)

def impulseSelection():
	pulses = ['Impulse 2', 'Impulse 4 (not implemented yet']
	functions = [getImpulse_2b]
	count = 1;
	selection = 0;

	for pulse in pulses:
		print("{0:d}) {1:s}".format(count, pulse))
		count = count + 1;

	selection = int(input('Funktion auswählen: '))

	while selection < 0 and selection > len(pulses) and not selection == 200:
		print('Bitte einen Wert zwischen 1 und {0:d} eingeben (200 Beenden).'.format(len(pulses)))

	return functions[selection - 1]

class ChecksumBuffer:

	def __init__(self):
		self._listOfChecksums = {}
		self._offset = b'\x00\x01'
		self._encoding = 'cp437'

	def _add(self, stringValue):
		listOfbytes = stringValue.encode(self._encoding)
		sumOfBytes = int()
		offset = b'\x01\x00'
		result = int()
		byteCount = int()
		ret = str()

		for b in listOfbytes:
			sumOfBytes = sumOfBytes + b
		# Byte-Anzahl bestimmen 
		byteCount = 1 if round(sumOfBytes.bit_length() / 8) == 0 else round(sumOfBytes.bit_length() / 8) + 1
		result = int.from_bytes(offset, byteorder='big', signed=False) - sumOfBytes.to_bytes(byteCount, byteorder="big")[1]
		print("Checksum::getVDSChecksum sumOfBytes: '{sum:d}' (Byte Anzahl: {byteCount:d}) and result {result:d} for value '{val:s}'".format(sum = sumOfBytes, byteCount = byteCount, result=result, val = stringValue))

		ret = (result.to_bytes(1, byteorder="big").decode(self._encoding)).replace(' ', '')
		return ret


		# bytelist = value.encode('cp437')
		# bytecount = len(value)
		# # Summiere alle Dezimalwerte der Zeichen
		# sum = 0;
		# for b in bytelist:
		# 	sum = sum + b
		# print('Sum {sum:d}'.format(sum = sum))
		

		# # Offset als int (Hexadezimal = 100H) - errechnet Wert als int
		# result = int.from_bytes(self._offset, byteorder = 'little', signed = False) - sum.to_bytes(2, byteorder = 'little', signed = False)[0]
		# print('result: {result:d}'.format(result = result))
		
		# if result == 0:
		# 	result = result + 256
		# elif result == 10:
		# 	result = result + 266

		# print('result: {result:d}'.format(result = result))
		# c = result.to_bytes(1, byteorder = 'little', signed=False)
		# print(type(c))
		# print(c)
		# self._listOfChecksums[value] = c
		# c = c.decode('cp437')

		# return c



		
	def get(self, value):


		if value not in self._listOfChecksums.keys():
			#print('Der Wert {0:s} ist noch nicht im Puffer'.format(value))
			return self._add(value)

		return self._listOfChecksums[value]


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

class VisaHelper:

	@staticmethod
	def selectResource():
		rm = visa.ResourceManager()
		res_list = rm.list_resources()
		c = 0
		selection = int(0)

		for res in res_list:
			print('({num:4}){res:30}'.format(res=res, num = c))
			c = c + 1
		print('(200) Abbrechen')

		selection = int(input("Resource auswählen: "))

		while selection < 0 and selection > len(res_list) - 1 and not selection == 200:
			selection = int(input("Resource auswählen: "))
			
		return res_list[selection]			

if __name__ == '__main__':
    main()
