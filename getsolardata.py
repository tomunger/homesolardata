from time import sleep
import requests
import datetime
import traceback
import csv

'''
Original data logger.  

Read from the local envoy system (known data points) and write to a local csv file.
'''

while True:
	data = None

	try: 
		# download json from URL
		r = requests.get('http://envoy.local/ivp/meters/readings')

		# parse json
		data = r.json()
	except Exception as e:
		print ("Exception reading data: \n", str(e))
		print (traceback.format_exc())


	if data is not None:
		production = data[0]['activePower']
		net = data[1]['activePower']
		consumption = production + net

		print (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {consumption:.1f} - {production:.1f} -> {net:.1f}")

		# 
		# Open the file each time so that data is not lost on crash.
		#
		try: 
			with open("solardata.csv", "a") as f:
				writer = csv.writer(f)
				writer.writerow([datetime.datetime.now().isoformat(), consumption, production, net])
		except Exception as e:
			print ("Exception writing data: \n", str(e))
			print (traceback.format_exc())


	sleep(60)

