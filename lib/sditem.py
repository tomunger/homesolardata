from datetime import datetime 

class SDItem(object):
	'''
	A single solar data item.
	'''
	def __init__(self, time: datetime, production: float, consumption: float):
		self.time = time
		self.production = production
		self.consumption = consumption

	def __str__(self):
		return f"{self.time},{self.production},{self.consumption}"

