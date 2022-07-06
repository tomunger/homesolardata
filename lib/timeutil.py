import datetime

def beginningOfDay(dt):
	return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def endOfDay(dt):
	return beginningOfDay(dt) + datetime.timedelta(1)
