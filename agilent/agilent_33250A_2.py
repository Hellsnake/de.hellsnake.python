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
	visa_dev = object
	current_field_raise = 75
	magnetic_resistance = 0.15
	source_multiplier = 5.6
	params = dict()
	start_magneticfield = float(input('Startmagnetfeldstärke [A/m]:'))
	end_magneticfield = float(input('Endmagnetfeldstärke [A/m]: '))
	dc_offset = float(input('DC-Offset [V]: '))
	start_frequency = float(input('Startfrequenz [Hz]: '))
	stop_frequency = float(input('Stopfrequenz [Hz]: '))
	step_size = float(input('Schrittweite [Hz]: '))
	dwell_time = float(input('Verweilzeit [s]: '))
	answer = str()
	response = str()
	start_time = 0
	end_time = 0

	params['start_magneticfield'] = start_magneticfield
	params['end_magneticfield'] = end_magneticfield
	params['dc_offset'] = dc_offset
	params['start_frequency'] = start_frequency
	params['stop_frequency'] = stop_frequency
	params['step_size'] = step_size
	params['dwell_time'] = dwell_time

	print('Parameter'.center(100,'-'))
	print('{0:30} {0:20}\n'.format('Parameter', 'Wert'))

	for k, v in params.items():
		print('{0:30} {1:8.4f}'.format(k, v))
	print('\n' + ''.center(100, '-'))

	visa_dev = getDevice()
	response = visa_dev.query("*IDN?")
	if '33250A' not in response:
		print('Bei dem Gerät handelt es sich nicht um ein Agilent 33250A, sondern um das {0:s}\n'.format(response))
		exit()

	print('VISA-Gerät: {0:s}\n'.format(response))

	print(''.center(100, '-'))

	answer = str(input('Vorgang starten?[j[or press Enter]/n]?'))

	if answer == 'n' or answer == 'N':
		print('Beende...')
		exit()


	response = visa_dev.query('DISP?')

	if '1' in response:
		answer = str(input('Display ist an! Soll es ausgeschalten werden? (Signalgenerator reagiert dadurch etwas schneller)'))
		if answer == 'j' or answer == 'J':
			time.sleep(1)
			visa_dev.write('DISP OFF')

	
	counter = params['start_frequency']
	start_time = time.time()
	start_voltage = ((params['start_magneticfield'] / current_field_raise) * magnetic_resistance) / source_multiplier
	offset = start_voltage * 1.41
	print('Setze den Ausgangswiderstand auf 10 kohm\n')
	visa_dev.write('OUTP:LOAD 10000')
	while  counter <= params['stop_frequency']:
		visa_dev.write('APPL:SIN {freq} HZ, {start_voltage} Vrms, {offset} V'.format(freq=counter, start_voltage = start_voltage, offset = offset))
		#visa_dev.write('DISP:TEXT' + '"Testspannung: ' + str(counter) + '"')
		counter = counter + params['step_size']
		time.sleep(params['dwell_time'])
		sys.stdout.write('aktuelle Frequenz: {0:8.4f} Hz, bisherige Prüfdauer: {1:8.2f} s\r'.format(counter, time.time() - start_time))
		sys.stdout.flush()

	# Status des Ausganges überprüfen
	response = visa_dev.query('OUTP?')
	if '1' in response:
		print('Ausgang wird abgeschalten...\n')
		visa_dev.write('OUTP OFF')


	print('Test beendet mit Frequenz {0:8.4f} Hz und einer Prüfdauer von {1:8.2f} s\n'.format(counter, time.time() - start_time))
	# Display Ausgabe zurücksetzen
	visa_dev.write('DISP:TEXT:CLEAR')
	visa_dev.close() # Gerät schließen
	exit()


def getDevice():
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

	return visa_dev

if __name__ == '__main__':
    main()
