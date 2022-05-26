
from ipaddress import ip_address
import socket
import requests
import logging
import datetime

import sditem


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



class SDFetch(object):


	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.ip_address = None
		self.next_ip_fetch = datetime.datetime.now()
		self.ipaddr_refresh_interval = datetime.timedelta(minutes=2)



	def getSDItem(self) -> sditem.SDItem:
		self._reffetch_ipaddr()

		item = None

		try:
			item = self._get_from_host(self.host, self.port)
		except requests.exceptions.ConnectionError as e:
			logger.info("Trying to fetch from by address %s:%d", self.ip_address, self.port)
			try:
				item = self._get_from_host(self.ip_address, self.port)
			except Exception as e:
				logger.error("Trying to fetch by addresse failed: %s", str(e))

		return item


	def _reffetch_ipaddr(self):
		if self.next_ip_fetch <= datetime.datetime.now():
			try:
				self.ip_address = socket.gethostbyname(self.host)
			except Exception:
				pass
			else:
				self.next_ip_fetch = datetime.datetime.now() + self.ipaddr_refresh_interval



	def _get_from_host(self, host, port) -> sditem.SDItem:
		'''
		Read a data item from the local envoy system
		
		Parameters:
			host: The hostname or IP address of the envoy system
			port: The port number of the envoy system

		Returns:
			An SDItem object with current producton and cunsumption data

		raises:
			requests.exceptions.ConnectionError: the connection failed.

		'''
		rjson = None
		item = None
		url = f'http://{host}:{port}/ivp/meters/readings'
		try: 
			# download json from URL
			r = requests.get(url, timeout=10)

			# parse json
			rjson = r.json()
		except requests.exceptions.Timeout:
			# This probably represents network issues that won't succeed with second try
			logger.error ("Timeout reading Enphase data from %s:%d", host, port)
		except requests.exceptions.ConnectionError:
			# This, sometimes, represent problems looking up the hostname, and my succeed if done with an IP address.
			logger.error ("Connection error reading Enphase data from %s:%d", host, port)
			raise
		except Exception as e:
			# This is an unknown error.
			logger.error ("Exception reading data from %s:%d: %s\n", host, port, str(e), exc_info=True)


		if rjson is not None:
			production = rjson[0]['activePower']
			net = rjson[1]['activePower']
			consumption = production + net
			item = sditem.SDItem(datetime.datetime.now(), consumption, production)

		return item

