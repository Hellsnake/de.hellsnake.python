import visa
import time

class PyVisa_Helper:

	@staticmethod
	def selectDevice():
		visa_rm = visa.ResourceManager()
		visa_devlist = visa_rm.list_resources()
		count = int(0)
		
		
		print('Angeschlossenen Geräte'.center(100, '-'))
		for dev in visa_devlist:
			print('({0:d}) {1:s}\n'.format(count, dev))
			count = count + 1
		print(''.center(100, '-'))

		# Kein Gerät gefunden
		if len(visa_devlist) == 0:
			print('Kein Gerät gefunden! Beende...')
			return

		dev_select = -1
		while dev_select < 0 or dev_select > len(visa_devlist):
			dev_select = int(input('Gerät auswählen(0...x, [> 30] => Abbrechen): '))
			if dev_select > 30:
				return

		print(visa_devlist[dev_select])

		visa_dev = visa_rm.open_resource(visa_devlist[dev_select])
		time.sleep(1)
		if not visa_dev:
			print('Kann Gerät nicht verbinden! Beende....')
			return

		print('Folgendes Gerät ausgewählt:'.center(100, '-'))

		return visa_dev