import logging
from logging.handlers import RotatingFileHandler
import json
import time
import threading
import sys
import requests
import datetime
import queue


import sdlogger
import sditem
import random

'''
Solar data logger.

This system reads from my local Enphase envoy and writes to a dattabase.

The two steps are handled in separate threads so that delays while writing to the database don't
delay collection of data points.  

If the database is unavailable, data points are stored in a local CSV file and transmitted
next time the database is available.
'''

# Get configuration
with open("localconfig.json", "r") as f:
	config = json.load(f)




#
# Configure logging to a rotating file and to console
#
rootLogger = logging.getLogger('')
# Don't call:  rootLogger.setLevel(logging.DEBUG) --- this will allow logging from other imported modules to come through.

# A formatter can be shared across handlers.
sharedformatter = logging.Formatter('%(asctime)s:%(threadName)s:%(name)s:%(levelname)s:  %(message)s')

# Rotating file handler
rfHandler = RotatingFileHandler("local_sdlog.txt", maxBytes=1000000, backupCount=5)
rfHandler.setFormatter(sharedformatter)
rfHandler.setLevel(logging.INFO)
rootLogger.addHandler(rfHandler)

# Console handler that will report only warnings.
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(sharedformatter)
consoleHandler.setLevel(logging.WARN)
rootLogger.addHandler(consoleHandler)

# Create logger for this module.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



class SDLoggerThread(object):
	'''
	Read log items from a queue and log them
	'''
	def __init__(self, q, solarloger: sdlogger.SDLogger):
		self.queue = q
		self.solarlogger = solarloger

	def run(self):
		while True:
			# Get the next work item
			item: sditem.SDItem = self.queue.get()

			# Termination Signal?
			if item is None:
				self.queue.task_done()
				logger.warning("LoggerThread exiting")
				return

			# Process the work item
			try:
				self.solarlogger.log_item(item)
			except Exception as e:
				logger.error("Unexpected exception from solar logger: %s", str(e), exc_info=True)

			# Signal completion
			self.queue.task_done()




def getSDItem() -> sditem.SDItem:
	'''
	Read a data item from the local envoy system
	TODO:  Move this to a class that will interrogate the Enphase system and return correct values
		for other installations.
	'''
	rjson = None
	item = None
	try: 
		# download json from URL
		r = requests.get('http://envoy.local/ivp/meters/readings')

		# parse json
		rjson = r.json()
	except Exception as e:
		logger.error ("Exception reading data: \n", str(e), exc_info=True)


	if rjson is not None:
		production = rjson[0]['activePower']
		net = rjson[1]['activePower']
		consumption = production + net

		item = sditem.SDItem(datetime.datetime.now(), consumption, production)

	return item





logger.info("----- STARTING -----")


#
# Create the solar logger
#
sdlogger = sdlogger.SDLogger("local_cache.csv", 
				config['dbname'],
				config['dbtable'],
				config['dbuser'],
				config['dbpass'], 
				config['dbhost'], 
				config['dbport'])


#
# Create a thread to do the logging
#
q = queue.Queue()
c = SDLoggerThread(q, sdlogger)
t = threading.Thread(target=c.run)
t.start()




#
# Main thread then loops forever
try:
	while True:
		item = getSDItem()
		if item is not None:
			q.put_nowait(item)
			print (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {item.consumption:.1f} - {item.production:.1f} -> {item.production - item.consumption:.1f}")
		else:
			print (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: no data captured")
		# TODO:  more precise sleep time so we are closer to every even 10 seconds.
		time.sleep(10)
except KeyboardInterrupt:
	logger.warning ("Keyboard interrupt")



#
# clean up
#
logger.warning ("Sending termination signal")
q.put_nowait(None)

logger.warning ("Waiting for logger thread")
t.join()

logger.warning("----- ENDING -----")
logging.shutdown()