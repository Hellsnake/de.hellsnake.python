import visa
import time
import sys

class TestParameter(object):
	'''docstring for ClassName'''
	def __init__(self):
		super(ClassName).__init__()
		self.arg = arg
		self.__values = dict()

	def add(self, key, value):
		self.__values[key] = value


def main():
	amp_scale = float(6.0) # Verstärkung des VDS
	# Der Offset dient für die "Nullung" der Spannung, da der Signalgenerator nicht genau 0 V herausgibt
	# Wenn am Signalgenerator 0 V anliegen, dann kommen rund 8 mV am VDS heraus.
	offset = -0.0012 
	params = dict()
	start_voltage = float(input('Startspannung am VDS eingeben (in V): '))
	end_voltage = float(input('Endspannung am VDS auswählen (in V): '))
	step_size = float(input('Schrittweite am VDS: (V/min): '))
	answer = str()
	response = str()
	start_time = 0
	end_time = 0

	params['start_voltage'] = start_voltage
	params['start_voltage_signalgen'] = start_voltage / amp_scale
	params['end_voltage'] = end_voltage
	params['end_voltage_signalgen'] = end_voltage / amp_scale
	params['step_size'] = step_size
	params['steps_size_signalgen'] = round(step_size / amp_scale / 60, 3)
	params['step_per_second'] = round((step_size / 60), 3)


	print('Parameter'.center(100,'-'))
	print('{0:30} {0:20}\n'.format('Parameter', 'Wert'))

	for k, v in params.items():
		print('{0:30} {1:8.4f}'.format(k, v))
	print('\n' + ''.center(100, '-'))

	print("ungefähre Prüfungsdauer: {0:8.2f} Minuten,"  
		"Schrittanzahl: {1:8.2f} ".format(abs(params['start_voltage_signalgen'] - 
			params['end_voltage_signalgen']) / params['steps_size_signalgen'] / 60, 
			abs(start_voltage - end_voltage) / params['step_per_second']))

	visa_rm = visa.ResourceManager()
	visa_devlist = visa_rm.list_resources()

	print('Angeschlossenen Geräte'.center(100, '-'))
	print(visa_devlist)
	print(''.center(100, '-'))

	# Kein Gerät gefunden
	if len(visa_devlist) == 0:
		print('Kein Gerät gefunden! Beende...')
		exit()

	dev_select = -1
	while dev_select < 0 or dev_select > len(visa_devlist):
		dev_select = int(input('Gerät auswählen(0...x, [> 30] => Abbrechen): '))
		if dev_select > 30:
			exit()

	print(visa_devlist[dev_select])

	visa_dev = visa_rm.open_resource(visa_devlist[dev_select])
	time.sleep(1)
	if not visa_dev:
		print('Kann Gerät nicht verbinden! Beende....')
		exit()

	print('Folgendes Gerät ausgewählt:'.center(100, '-'))
	print(visa_dev.query("*IDN?"))
	print(''.center(100, '-'))

	answer = str(input('Vorgang starten?[j/n]?'))

	if answer == 'n' or answer == 'N':
		print('Beende...')
		exit()

	step_per_second = params['step_per_second']

	response = visa_dev.query('DISP?')

	if '1' in response:
		answer = str(input('Display ist an! Soll es ausgeschalten werden? (Signalgenerator reagiert dadurch etwas schneller)'))
		if answer == 'j' or answer == 'J':
			time.sleep(1)
			visa_dev.write('DISP OFF')

	
	start = params['start_voltage_signalgen']
	stop = params['end_voltage_signalgen']
	step = params['steps_size_signalgen']

	# Von unterer Spannung zur oberen 
	counter = 0

	if start < stop:
		counter = start - offset
		start_time = time.time()
		while  counter < stop:
			visa_dev.write('APPL:DC DEF, DEF, ' + str(counter))
			#visa_dev.write('DISP:TEXT' + '"Testspannung: ' + str(counter) + '"')
			counter = counter + step
			time.sleep(1.3)
			sys.stdout.write('aktuelle Spannung: {0:8.4f} V, Zeit: {1:8.2f} s\r'.format(counter, time.time() - start_time))
			sys.stdout.flush()
	# von oberer Spannung zur unteren 
	elif start > stop:
		counter = start
		while counter > stop:
			visa_dev.write('APPL:DC DEF, DEF, ' + str(counter))
			# visa_dev.write('DISP:TEXT' + '"Testspannung: ' + str(counter) + '"')
			counter = counter - step
			time.sleep(1.3)
			sys.stdout.write('aktuelle Spannung: {0:8.4f} V, Zeit: {1:8.2f} s\r'.format(counter, time.time() - start_time))
			sys.stdout.flush()

	print('Test beendet mit Spannung {0:8.4f} V und einer Prüfdauer von {1:8.2f} s'.format(counter, time.time() - start_time))
	# Display Ausgabe zurücksetzen
	visa_dev.write('DISP:TEXT:CLEAR')
	visa_dev.close() # Gerät schließen
	exit()

if __name__ == '__main__':
    main()
