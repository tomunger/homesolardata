
from ipaddress import ip_address
import socket
import requests
import logging
import datetime

import sditem
import evsystem


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



class SDFetch(object):


	def __init__(self, ev: evsystem.EVSystem):
		self._ev: evsystem = ev



	def getSDItem(self) -> sditem.SDItem:
		item = None
		
		pc = self._ev.get_power()
		if pc is not None:
			item = sditem.SDItem(datetime.datetime.now(), pc[0], pc[1])

		return item

