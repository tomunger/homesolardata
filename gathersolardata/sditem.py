from datetime import datetime 

class SDItem(object):
	'''
	A single solar data item.
	'''
	def __init__(self, time: datetime, consumption: float, production: float):
		self.time = time
		self.consumption = consumption
		self.production = production

	def __str__(self):
		return f"{self.time},{self.consumption},{self.production}"

