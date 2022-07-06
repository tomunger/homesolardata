'''
Abstract EVsystem class
'''
from typing import Tuple

class EVSystem(object):
	def get_power(self) -> Tuple[float, float]:
		raise NotImplementedError()


class EVSystemException(Exception):
	pass