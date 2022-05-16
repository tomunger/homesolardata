import smtplib
from email.message import EmailMessage
import email.utils
import json

# Get configuration
with open("localconfig.json", "r") as f:
	config = json.load(f)

port = 465

username = 'x'
password = "x"
try:
	smtp = smtplib.SMTP(config['mailhost'], config['mailport'], timeout=15)
	msg = EmailMessage()
	msg['From'] = config['mailfrom']
	msg['To'] = config['mailto'] 
	msg['Subject'] = 'test send'
	msg['Date'] = email.utils.localtime()
	msg.set_content('sample message\nplease read')
	if username:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()
		smtp.login(username, password)
	smtp.send_message(msg)
	smtp.quit()
except Exception as e:
	print(e)

