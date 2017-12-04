import visa

'''
Model Class for Visa Devices
'''

class DeviceModel(Object):

	def _init_(self):
		try:
			self._rm = visa.ResourceManager()
		except (VisaIOError, Error):
			
		self._listener = []


	def add_Listener(self, listener):
		if None != listener:
			_listener.append(listener)

	def remove_Listener(self, listener):
		if None != listener:
			_listener.remove_Listener(listener)


	def raise_error(self, Error):
		for l in self._listener:
			

			