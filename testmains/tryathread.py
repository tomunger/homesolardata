import queue
import select
import sys
import re
import time
import logging
import traceback

import threading

'''
Example of how to implement a readder thread and pass work items to it.
'''

class Message(object):
	'''
	A class that represents work placed on queue.
	'''
	def __init__(self, msg):
		self.msg = msg

	


class Consumer(object):
	'''
	The worker thread, on a class with associated attributes.
	run() method reads from queue and processes.  
	Sending None to queue will cause run() to exit.
	'''
	def __init__(self, queue):
		self.queue = queue

	def run(self):
		while True:
			# Get the next work item
			work_item = self.queue.get()

			# Termination Signal?
			if work_item is None:
				self.queue.task_done()
				print ("Consumer: got None")
				return

			# Process the work item
			print(f"Processing: '{work_item.msg}'")
			time.sleep(2)
			print(f"Processing: '{work_item.msg}' complete")

			# Signal completion
			self.queue.task_done()




def poll_nix(skt):
	''' Blocking poll for input.
	'''
	i,o,e = select.select([skt],[],[])
	for s in i:
		if s == skt:
			v = skt.readline()
			return re.sub("[\r\n]", '', v)
	return None



#
# Crate the queue, a consumer to read from the queue, and a thread to run the consumer.
#
q = queue.Queue()
c = Consumer(q)
t = threading.Thread(target=c.run)


#
# Start the consumer thread then read text from the terminal
#
t.start()

while True:
	try:
		print ("> ", end='', flush=True)
		data = poll_nix(sys.stdin)
	except KeyboardInterrupt:
		print("Keyboard interrupt")
		break
	if data is not None:
		q.put_nowait(Message(data))
		if data == 'quit':
			break


#
# clean up
#
print ("Sending termination signal")
q.put_nowait(None)

print ("joining queue")
t.join()
print ("Exiting")