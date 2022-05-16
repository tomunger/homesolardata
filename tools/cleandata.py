import csv

'''
Clean a CSV file.

Read solar data fields are

time, consumption, production, net

round consumption and production to 1 decimal place.  Remove net - it can be calculated as the difference.

'''

with open("local-solardata.csv", "r") as fdin:
	reader = csv.reader(fdin)
	with open("local-new-solardata.csv", "w") as fdout:
		writer = csv.writer(fdout)
		for row in reader:

			# Clean up:  
			row[1] = str(round(float(row[1]),1))
			row[2] = str(round(float(row[2]),1))
			writer.writerow(row[0:3])
