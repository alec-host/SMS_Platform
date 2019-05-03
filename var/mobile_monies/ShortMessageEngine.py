#!/usr/bin/python
"""
developer skype: alec_host
"""
import os
import time
import Queue
import threading

import logging

from conn.dbhelper import create_connection,close_connection,NoResultException
from conn.model import _process_sms

import MySQLdb

logger = logging.getLogger()

def main(): 
	try:
		while True:
			"""
			open MySQL connection
			"""
			db = create_connection()
			"""
			.
			"""
			q = Queue.Queue()

			t = threading.Thread(target=_process_sms,args = (q,db))
		
			t.daemon = True
			t.start()
			
			time.sleep(.5)
	except MySQLdb.Error, e:
		logger.error(e)
	except Exception, e:
		logger.error(e)
	finally:
		try:
			if not db:
				exit(0)
			else:
				"""
				close MySQL connection.
				"""			
				close_connection(db)
		except MySQLdb.Error, e:
			logger.error(e)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit();
	
	