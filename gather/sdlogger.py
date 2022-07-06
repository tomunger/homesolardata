import pymysql
import logging
import datetime
import pathlib
import csv
import iso8601
from typing import List

from sditem import SDItem

'''
Class that will write solar data items to a database.  When
the database is unaviablable, cache the items in a CSV file.
'''


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class data_set(object):

	def __init__(self):
		self.data = []
		self.new_count = 0
		self.old_count = 0
		self.transmitted_count = 0

	def add_new(self, item: SDItem):
		self.data.append(item)
		self.new_count += 1

	def add_old(self, item: SDItem):
		self.data.append(item)
		self.old_count += 1

	
	

def timestampname(original_name: pathlib.Path) -> pathlib.Path:
	'''
	Create a new file name with a timestamp.
	'''
	ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
	return original_name.parent / (original_name.stem + '_' + ts + original_name.suffix)	


class SDLogger(object):
	'''
	The worker thread, on a class with associated attributes.
	run() method reads from queue and processes.  
	Sending None to queue will cause run() to exit.
	'''
	def __init__(self, local_cache_file: str, db_name: str, db_table: str, db_user: str, db_pass: str, db_host: str, db_port: int):
		self.local_cache_file = pathlib.Path(local_cache_file)
		self.db_name = db_name
		self.db_table = db_table
		self.db_user = db_user
		self.db_pass = db_pass
		self.db_host = db_host
		self.db_port = db_port
		self._report_time = datetime.datetime.now()
		self._report_interval = datetime.timedelta(minutes=30)
		self._sent_count = 0
		logger.info(f"Logging data to {db_host}:{db_port}, user {db_user}, {db_name}/{db_table}")


	def run(self):
		while True:
			# Get the next work item
			sd_item: SDItem = self.queue.get()

			# Termination Signal?
			if sd_item is None:
				self.queue.task_done()
				logger.info ("Got termination signal")
				return

			# Process the work item
			logger.debug ("Processing: %s", str(sd_item))
			self.log_item(sd_item)


			# Signal completion
			self.queue.task_done()



	def log_item(self, sd_item: SDItem):
		'''
		Log the item to the local cache file.
		'''
		data =  data_set()

		#
		# Load the cache file.
		#
		if self.local_cache_file.exists():
			self._cache_load(data)


		#
		# Add the new item to the data set.
		#
		data.add_new(sd_item)


		#
		# Transmit
		#
		self._transmit(data)

		#
		# Saved un-sent data
		#
		self._cache_save(data)

		# Report periodically
		n = datetime.datetime.now()
		if n > self._report_time:
			logger.info("Transmitted %d items", self._sent_count)
			self._report_time = n + self._report_interval

					




	def _cache_load(self, data: data_set):
		'''
		Read the local cache file into data object as old items.
		'''
		try:
			with self.local_cache_file.open("r") as f:
				reader = csv.reader(f)
				for row in reader:
					if len(row) == 3:
						try:
							t = iso8601.parse_date(row[0])
							c = float(row[1])
							p = float(row[2])
							sd_item = SDItem(t, c, p)
							data.add_old(sd_item)
						except Exception as e:
							logger.error("Failed to parse row: %s", e)
							continue
					else:
						logger.error("Failed to parse row: %s", row)
		except Exception as e:
			logger.error("Failed to load cache file: %s", e, exc_info=True)
			# Rename the file in case it is corrupted.
			try:
				self.local_cache_file.rename(timestampname(self.local_cache_file))
			except Exception as e:
				logger.error("Failed to rename cache file: %s", e)
		if data.old_count > 0:
			logger.info("Loaded %d old items from cache file", data.old_count)




	def _transmit(self, data: data_set):
		'''
		Write the list of items to the database.
		'''	
		try:
			connection = pymysql.connect(host=self.db_host,
										user=self.db_user,
										password=self.db_pass,
										database=self.db_name,
										charset='utf8mb4',
										cursorclass=pymysql.cursors.DictCursor)
		except Exception as e:
			logger.error("Failed to connect to database: %s", e, exc_info=False)
			return

		logger.debug("send %d old and %d new items to database", data.old_count, data.new_count)
		with connection:
			# TODO:  Change to executemany() but consider max statement size.
			sql = f"insert into `{self.db_table}` (`datetime`, `consumption`, `production`) VALUES (%s, %s, %s)"
			with connection.cursor() as cursor:
				for item in data.data:
					t = item.time.strftime('%Y-%m-%d %H:%M:%S.%f')
					try:
						cursor.execute(sql, (t, item.consumption, item.production))
						data.transmitted_count += 1
					except Exception as e:
						logger.error("Failed to execute sql: %s", e, exc_info=True)
						return
					if data.transmitted_count % 500 == 0:
						logger.debug("...Transmitted %d items", data.transmitted_count)

			try:
				connection.commit()
			except Exception as e:
				logger.error("Failed to commit transaction: %s", e, exc_info=True)
				data.transmitted_count = 0
			# Log at lower level when other than standard case of 1 item transmitted.
			logger.log(logging.DEBUG if data.transmitted_count == 1 else logging.INFO,
						"%d items transmitted", data.transmitted_count)

			self._sent_count += data.transmitted_count



	
	def _cache_save(self, data: data_set):
		'''
		Save the list of items to the local cache file.
		'''
		#
		# Append to existing file or create a new one?
		#
		if data.transmitted_count == len(data.data):
			#
			# All transmitted, remove cache file
			#
			if self.local_cache_file.exists():			
				logger.info("no items to cache, delete cache file")
				try:
					self.local_cache_file.unlink()
				except Exception as e:
					# TODO:  Notify fatal error
					logger.error("Failed to delete cache file: %s", e, exc_info=True)
					return

		else:
			#
			# Some transmitted, append to existing file.
			#
			savefrom = 0
			if self.local_cache_file.exists():
				if data.transmitted_count == 0:
					# Save new items only.
					savefrom = data.old_count
					logger.info("append %d items to cache file", len(data.data) - savefrom)
				else:
					logger.info("write %d items to new cache file", len(data.data))
					try:
						self.local_cache_file.unlink()
					except Exception as e:
						# TODO:  Notify fatal error
						logger.error("Failed to delete cache file: %s", e, exc_info=True)
						return
		
			if savefrom < len(data.data):
				with self.local_cache_file.open("a") as f:
					writer = csv.writer(f)
					for item in data.data[savefrom:]:
						writer.writerow([item.time.isoformat(), item.consumption, item.production])