import visa
import time
import sys
from visa_helper import PyVisa_Helper

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
	signal_gen_load = float(10000)
	# Der Offset dient für die "Nullung" der Spannung, da der Signalgenerator nicht genau 0 V herausgibt
	# Wenn am Signalgenerator 0 V anliegen, dann kommen rund 8 mV am VDS heraus.
	offset = -0.0012 
	min_voltage = 0.0000
	max_voltage = 60.0000
	params = dict()

	start_voltage = float(input('Startspannung am VDS eingeben (in V, min: {0:8.6f}, max: {1:8.6f})'.format(min_voltage, max_voltage)))
	end_voltage = float(input('Endspannung am VDS auswählen (in V, min: {0:8.6f}, max: {1:8.6f})'.format(min_voltage, max_voltage)))
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
	params['steps_size_signalgen'] = round(step_size / amp_scale / 60, 6)
	params['step_per_second'] = round((step_size / 60), 6)


	print('Parameter'.center(100,'-'))
	print('{0:30} {0:20}\n'.format('Parameter', 'Wert'))

	for k, v in params.items():
		print('{0:30} {1:8.6f}'.format(k, v))
	print('\n' + ''.center(100, '-'))

	# Start und Stop sind gleich groß --> Hoch - und runterfahren
	if(start_voltage == end_voltage):
		step_count = (params['start_voltage'] * 2) / params['step_per_second']
		test_duration = (abs(params['start_voltage_signalgen'] / params['steps_size_signalgen']) / 60) * 2
	else:
		step_count = abs((start_voltage - end_voltage) / params['step_per_second'])
		test_duration = abs(params['start_voltage_signalgen'] - params['end_voltage_signalgen']) / params['steps_size_signalgen'] / 60

	print("ungefähre Prüfungsdauer: {0:8.2f} Minuten, Schrittanzahl: {1:8.2f} ".format(test_duration, step_count))

	visa_dev = PyVisa_Helper.selectDevice()
	if not visa_dev:
		print('Kann Gerät nicht verbinden! Beende....')
		exit()

	print('Folgendes Gerät ausgewählt:'.center(100, '-'))
	response = visa_dev.query('*IDN?')
	print(response)
	print(''.center(100, '-'))

	if('33250A' not in response):
		print('Agilent 33250A nicht ausgewählt, beende ...')
		exit()

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
	print('Startzeit: {0:s}'.format(time.strftime("%d-%m-%Y, %H:%M:%S", time.gmtime())).center(100,'-'))
	print('Setze den Ausgangswiderstand auf {0:8.2f} ohm\n'.format(signal_gen_load))
	visa_dev.write('OUTP:LOAD 10000')
	# Von unterer Spannung zur oberen 
	counter = 0
	print('Spannung Agilent [V]\tSpannung VDS [V]\taktuelle benötigte Zeit [s]')
	if start < stop:
		counter = start - offset
		start_time = time.time()
		while  counter < stop:
			visa_dev.write('APPL:DC DEF, DEF, ' + str(counter))
			#visa_dev.write('DISP:TEXT' + '"Testspannung: ' + str(counter) + '"')
			counter = counter + step
			time.sleep(1.0)
			sys.stdout.write('{0:8.6f}\t\t {1:8.6f}\t\t {2:8.6f} \r'.format(counter, counter * amp_scale, time.time() - start_time))
			sys.stdout.flush()
	# von oberer Spannung zur unteren 
	elif start > stop:
		counter = start
		start_time = time.time()
		while counter > stop:
			visa_dev.write('APPL:DC DEF, DEF, ' + str(counter))
			# visa_dev.write('DISP:TEXT' + '"Testspannung: ' + str(counter) + '"')
			counter = counter - step
			time.sleep(1.0)
			sys.stdout.write('{0:8.6f}\t\t {1:8.6f}\t\t {2:8.6f} \r'.format(counter, counter * amp_scale, time.time() - start_time))
			sys.stdout.flush()
	#Hoch --> Runter --> Hoch
	elif start == stop:
		counter = start
		start_time = time.time()
		while counter > 0:
			visa_dev.write('APPL:DC DEF, DEF, ' + str(counter))
			# visa_dev.write('DISP:TEXT' + '"Testspannung: ' + str(counter) + '"')
			counter = counter - step
			time.sleep(1.0)
			sys.stdout.write('{0:8.6f}\t\t {1:8.6f}\t\t {2:8.6f} \r'.format(counter, counter * amp_scale, time.time() - start_time))
			sys.stdout.flush()
		counter = 0
		while  counter <= stop:
			visa_dev.write('APPL:DC DEF, DEF, ' + str(counter))
			#visa_dev.write('DISP:TEXT' + '"Testspannung: ' + str(counter) + '"')
			counter = counter + step
			time.sleep(1.0)
			sys.stdout.write('{0:8.6f}\t\t {1:8.6f}\t\t {2:8.6f} \r'.format(counter, counter * amp_scale, time.time() - start_time))
			sys.stdout.flush()
	print('Stopzeit: {0:s}'.format(time.strftime("%d-%m-%Y, %H:%M:%S", time.gmtime())).center(100,'-'))
		


	sys.stdout.write('{0:8.6f}\t {1:8.6f}\t\t {2:8.6f} \r'.format(counter, counter * amp_scale, time.time() - start_time))
	visa_dev.write('DISP:TEXT:CLEAR')
	answer = input('Ausgang abschalten?(j/n)')
	if('j' in answer or 'J' in answer):
		visa_dev.write('OUTP OFF')
	visa_dev.close() # Gerät schließen
	exit()

if __name__ == '__main__':
    main()
