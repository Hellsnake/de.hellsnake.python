

class BaseConfig(object):
	"""docstring for BaseConfig"""
	def __init__(self, name, value):
		super(BaseConfig, self).__init__()
		self._name = name
		self._value = value

		