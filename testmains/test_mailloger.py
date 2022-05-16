import logging
from logging.handlers import SMTPHandler, RotatingFileHandler	
import json

'''
An attempt to send error log messages via email.

Failed because, I believe, my email server reuires an TSL connect from the start
while the logging library makes a clear connection and uses STARTTSL
'''


# Get configuration
with open("localconfig.json", "r") as f:
	config = json.load(f)

smtphandler = SMTPHandler(( config['mailhost'], config['mailport']),
						config['mailfrom'],
						[ config['mailto'] ],
						config['mailsubjectprefix'],
						credentials=(config['mailuser'], config['mailpass']),
						secure=(),
						timeout=15)
smtphandler.setLevel(logging.ERROR)

filehandler = RotatingFileHandler("local_testlogger.log", maxBytes=10485760, backupCount=5)
consoleHandler = logging.StreamHandler()


logging.basicConfig(level=logging.DEBUG)


logging.getLogger('').addHandler(smtphandler)
logging.getLogger('').addHandler(filehandler)
logging.getLogger('').addHandler(consoleHandler)


logging.debug("This is a debug message")
logging.info("This is a info message")
logging.error("This is a error message")

print ("done")