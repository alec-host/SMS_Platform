#!/usr/bin/python

"""
developer skype: alec_host
"""
import time
import signal
import sys
import json
import eventlet
import logging
import MySQLdb
import MySQLdb.cursors

from datetime import datetime
from betvantage_config import logger,mysql_params
from db_conn import DB,NoResultException,NoServiceIDException

eventlet.monkey_patch()

db = DB()

"""
#-.read inbound sms.
"""
def _read_incoming_sms_db(connection,limit=1000):
	processFlag = 0
	try:
		qry = """
			  SELECT 
			 `ID`,`MSISDN`,`Message`,`ShortCode`
			  FROM
			  """+mysql_params['db']+""".`tbl_incoming_sms` 
			  WHERE 
			 `IsProcessed` = %s
			  ORDER BY 
			 `ID` ASC
			  LIMIT %s
			  """	
		params = (processFlag,limit,)
		in_sms = db.retrieve_all_data_params(connection, qry, params)
		
		return in_sms
	except Exception, e:
		logger.error(e)
		raise		
"""
#-.get the size the queue.
"""
def _sms_queue_cnt_db(connection, limit=1):
	processFlag = 0
	count = 0
	try:
		qry = """
			  SELECT 
			  COUNT(`ID`) AS cnt
			  FROM
			  """+mysql_params['db']+""".`tbl_incoming_sms` 
			  WHERE 
			 `IsProcessed` = %s
			  LIMIT %s
			  """	
		params = (processFlag,limit)
		rows   = db.retrieve_all_data_params(connection,qry,params)
							
		for row in rows:
			count = row['cnt']
			
		return count
	except Exception, e:
		logger.error(e)
		raise		
"""
#-.mark message[s] as processed.
"""
def _processed_inbound_sms_db(record_id, connection):
	processFlag = 1
	defaultValue = "'0'"
	try:
		if(record_id != defaultValue):
			qry = """
				  UPDATE 
				  """+mysql_params['db']+""".`tbl_incoming_sms` 
				  SET 
				 `DateModified` = %s, 
				 `IsProcessed` = %s
				  WHERE 
				 `ID` IN ("""+record_id+""") 
				  """
			params = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),processFlag)
			db.execute_query(connection, qry, params)
			
			connection.commit()
	except Exception, e:
		logger.error(e)
		print(e)
		raise
"""
#-.create new user.
"""	
def _register_on_sms_db(msisdn,connection):
	jsonString = None
	try:
		sql = """CALL """+mysql_params['db']+""".`sProqClientRegister`(%s)"""
		
		params = (msisdn)
		output = db.retrieve_all_data_params(connection,sql,params)	
		
		for data in output:
			jsonString = json.loads(data.get('json_result'))

	except Exception, e:
		logger.error(e)
		raise	
		
	return jsonString['RESULT']	
"""
#-.queue outgoing message.
"""	
def _queue_outgoing_sms_db(destination,source,message,connection):
	jsonString = None
	try:
		sql = """CALL """+mysql_params['db']+""".`sProqHandleOutboundSms`(%s,%s,%s)"""
		
		params = (destination,source,message)
		output = db.retrieve_all_data_params(connection,sql,params)	
		
		for data in output:
			jsonString = json.loads(data.get('json_result'))

	except Exception, e:
		logger.error(e)
		raise	
		
	return jsonString['RESULT']		
"""
#-.queue outgoing message.
"""	
def _verify_customer_db(msisdn,pin,connection):
	jsonString = None
	try:
		sql = """CALL """+mysql_params['db']+""".`sProqClientAuthentication`(%s,%s)"""
		
		params = (msisdn,pin)
		output = db.retrieve_all_data_params(connection,sql,params)	
		
		for data in output:
			jsonString = json.loads(data.get('json_result'))

	except Exception, e:
		logger.error(e)
		raise	
		
	return [jsonString['RESULT'],jsonString['INFO']]
"""
#-.queue outgoing message.
"""	
def _withdraw_cash_db(msisdn,amount,connection):
	jsonString = None
	try:
		sql = """CALL """+mysql_params['db']+""".`sProqClientWithdraw`(%s,%s)"""
		
		params = (msisdn,amount)
		output = db.retrieve_all_data_params(connection,sql,params)	
		
		for data in output:
			jsonString = json.loads(data.get('json_result'))

	except Exception, e:
		logger.error(e)
		raise	
		
	return jsonString['RESULT']
"""
#-.queue outgoing message.
"""	
def _place_bet_db(msisdn,amount,connection):
	jsonString = None
	try:
		sql = """CALL """+mysql_params['db']+""".`sProqClientPlaceBet`(%s,%s)"""
		
		params = (msisdn,amount)
		output = db.retrieve_all_data_params(connection,sql,params)	
		
		for data in output:
			jsonString = json.loads(data.get('json_result'))

	except Exception, e:
		logger.error(e)
		raise	
		
	return jsonString['RESULT']	
"""
#-.update bonus.
"""	
def _sync_bonus_db(msisdn,bonus,connection):
	jsonString = None
	try:
		sql = """CALL """+mysql_params['db']+""".`sProqClientUtiliseBonus`(%s,%s)"""
		
		params = (msisdn,amount)
		output = db.retrieve_all_data_params(connection,sql,params)	
		
		for data in output:
			jsonString = json.loads(data.get('json_result'))

	except Exception, e:
		logger.error(e)
		raise	
		
	return jsonString['RESULT']	
			
"""
#-.db routine connection.
"""
def create_connection():
	try:
		connection = MySQLdb.connect(host=mysql_params['host'],\
					 user=mysql_params['user'], passwd=mysql_params['passwd'],\
					 db=mysql_params['db'], cursorclass=MySQLdb.cursors.DictCursor)
	except MySQLdb.Error, e:
		logger.error(e)
		raise
	return connection
"""	
#-.db close connection.
"""
def close_connection(connection):
	try:
		connection.close()
	except MySQLdb.Error, e:
		logger.error(e)
		raise
