import io
import subprocess

from ipaddress import ip_address
import socket
import datetime
# requests import requests
import httpx
#import pycurl  # see https://stackoverflow.com/questions/25491090/how-to-use-python-to-execute-a-curl-command
import logging
from evsystem import EVSystem, EVSystemException
from sditem import SDItem


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



class EnvoyMeter(object):
	eid:int
	state:str
	measurmentType:str
	status:str

	def __init__(self, eid:int, state:str, measurementType:str, meteringStatus:str):
		self.eid = eid
		self.state = state
		self.measurementType = measurementType
		self.meteringStatus = meteringStatus

	def __str__(self):
		return (f"EnvoyMeter(eid={self.eid}, state={self.state}, measurementType={self.measurementType}, meteringStatus={self.meteringStatus})")



class EnvoySystem(EVSystem):
	_url_meters:str = "https://{host}:{port}/ivp/meters"
	_url_meters_readings:str = _url_meters + "/readings"

	def __init__(self, 
				host:str="envoy.local", 
				port:int=80, 
				api_key:str = ""):
		self._host = host
		self._port = port
		self._api_key = api_key
		self._p_address = None
		self._next_ip_fetch = datetime.datetime.now()
		self._ipaddr_refresh_interval = datetime.timedelta(minutes=2)
		self._host_list: list[str] = [self._host]
		self._is_interrogated: bool = False
		self._meters: dict[int, EnvoyMeter] = {}
		self._eid_production: int = 0
		self._eid_net_consumption: int = 0
		# requests self._session = requests.Session()

		self._make_call = self._make_call_httpx

		self._interrogate()



	def _get_ip_address(self):
		if self._next_ip_fetch <= datetime.datetime.now():
			self._host_list: list(str) = [self._host]			
			try:
				self._ip_address = socket.gethostbyname(self._host)
				if self._ip_address != self._host:
					self._host_list.append(self._ip_address)
			except Exception:
				pass
			else:
				self._next_ip_fetch = datetime.datetime.now() + self._ipaddr_refresh_interval



	# def _makecall_requests(self, url_base:str) -> dict[str,str] | list[dict[str,str]]:
	# 	self._get_ip_address()
	# 	rjson = {}
	# 	for h in self._host_list:
	# 		url = url_base.format(host=h, port=self._port)
	# 		logger.debug("Trying to fetch from %s", url)

	# 		headers: dict[str, str] = {}
	# 		if self._api_key:
	# 			headers["Authorization"] = f"Bearer {self._api_key}"
	# 		try: 
	# 			# download json from URL
	# 			r = self._session.get(url, headers=headers, timeout=10)

	# 			# parse json
	# 			rjson = r.json()
	# 			break

	# 		except requests.exceptions.Timeout:
	# 			# This probably represents network issues that won't succeed with second try
	# 			logger.error ("Timeout reading Enphase data from %s", url)
	# 			break

	# 		except requests.exceptions.ConnectionError as e:
	# 			# This, sometimes, represent problems looking up the hostname, and my succeed if done with an IP address.
	# 			logger.exception ("Connection error reading Enphase data from %s", url)
	# 			continue

	# 		except Exception as e:
	# 			# This is an unknown error.
	# 			logger.error ("Exception reading data from %s: %s\n", url, str(e), exc_info=True)
	# 			break

	# 	return rjson


	def _make_call_httpx(self, url_base:str) ->  dict[str,str] | list[dict[str,str]]:
		self._get_ip_address()
		rjson = {}
		for h in self._host_list:
			url = url_base.format(host=h, port=self._port)
			logger.debug("Trying to fetch from %s", url)

			headers: dict[str, str] = {}
			if self._api_key:
				headers["Authorization"] = f"Bearer {self._api_key}"


			try: 
				# download json from URL
				r = httpx.get(url, headers=headers, verify=False, timeout=10)
				r.raise_for_status()
				# parse json
				rjson = r.json()
				break

			except httpx.TimeoutException:
				# This probably represents network issues that won't succeed with second try
				logger.error ("Timeout reading Enphase data from %s", url)
				break

			except httpx.ConnectError as e:
				# This, sometimes, represent problems looking up the hostname, and may succeed if done with an IP address.
				logger.exception ("Connection error reading Enphase data from %s", url)
				continue

			except httpx.HTTPStatusError as e:
				logger.exception("HTTP Error %s reading Enphase data from %s", e.response.status_code, url)

			except Exception as e:
				# This is an unknown error.
				logger.exception ("Exception reading data from %s: %s\n", url, str(e))
				break

		return rjson



	# def _make_call_curl(self, url_base:str) ->  dict[str,str] | list[dict[str,str]]:
	# 	self._get_ip_address()
	# 	rjson = {}
	# 	for h in self._host_list:
	# 		url = url_base.format(host=h, port=self._port)
	# 		logger.debug("Trying to fetch from %s", url)


	# 		response = io.StringIO()

	# 		c = pycurl.Curl()
	# 		c.setopt(c.URL, url)
	# 		c.setopt(c.WRITEFUNCTION, response.write)
	# 		c.setopt(c.HTTPHEADER, ['Authorization',f"Bearer {self._api_key}"])
	# 		#c.setopt(c.POSTFIELDS, '@request.json')

	# 		try: 
	# 			# download json from URL
	# 			c.perform()
	# 			c.close()
	# 			jstr = response.getvalue()
	# 			response.close()
	# 			rjson = jstr
	# 			break

	# 		except Exception as e:
	# 			# This is an unknown error.
	# 			logger.exception ("Exception reading data from %s: %s\n", url, str(e))
	# 			break

	# 	return rjson
	

	def _make_call_shcurl(self, url_base:str) ->  dict[str,str] | list[dict[str,str]]:
		self._get_ip_address()
		rjson = {}
		for h in self._host_list:
			url = url_base.format(host=h, port=self._port)
			logger.debug("Trying to fetch from %s", url)

			command = [
				"curl", '-f', '-k', "-H" ,'Accept: application/json',
				'-H', f'Authorization: Bearer {self._api_key}', 
				'-X', 'GET', url					
			]

			cmdstr = " ".join(command)


			try: 
				# download json from URL
				jstr = subprocess.check_output(command)
				rjson = jstr
				break

			except Exception as e:
				# This is an unknown error.
				logger.exception ("Exception reading data from %s: %s\n", url, str(e))
				break

		return rjson

	def _interrogate(self):
		meter_json: list[dict[str,str]] = self._make_call(self._url_meters)
		if meter_json is None:
			return
		
		for m in meter_json:
			eid = m.get("eid", 0)
			state = m.get("state", "")
			measurementType = m.get("measurementType", "")
			meteringStatus = m.get("meteringStatus", "")
			if eid > 0 and measurementType:
				self._meters[eid] = EnvoyMeter(eid, state, measurementType, meteringStatus)

		if logger.isEnabledFor(logging.INFO):
			logger.info("Discovered meters")
			for m in self._meters.values():
				logger.info("%s", m)

		for m in self._meters.values():
			if m.measurementType == "production":
				# raise an exception if self._eid_production is already set
				if self._eid_production > 0:
					raise EVSystemException("Multiple production meters found")
				self._eid_production = m.eid
			elif m.measurementType == "net-consumption":
				# raise an exception if self._eid_production is already set
				if self._eid_net_consumption > 0:
					raise EVSystemException("Multiple net-consumption meters found")
				self._eid_net_consumption = m.eid

		if self._eid_production == 0:
			raise EVSystemException("No production meter found")
		if self._eid_net_consumption == 0:
			raise EVSystemException("No net-consumption meter found")


		self._is_interrogated = True



	def get_power(self) -> SDItem:
		if not self._is_interrogated:
			self._interrogate()
		
		power_json = self._make_call(self._url_meters_readings)
		if power_json is None:
			return None
	
		production = 0.0
		consumption = 0.0
		for n in power_json:
			if n["eid"] == self._eid_production:
				production = n['activePower']
			elif n["eid"] == self._eid_net_consumption:	
				net = n['activePower']
			
		consumption = production + net

		item = SDItem(datetime.datetime.now(), production, consumption)
				
		return item
