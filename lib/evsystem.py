'''
Abstract EVsystem class
'''
import sditem

class EVSystem(object):
	def get_power(self) -> sditem.SDItem:
		raise NotImplementedError()


class EVSystemException(Exception):
	pass