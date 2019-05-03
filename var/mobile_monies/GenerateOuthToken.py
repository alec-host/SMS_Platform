#!/usr/bin/python

"""
"""
import os
import logging

from mpesa.gateway import oauth_generate_token,Mpesa
from conn.dbhelper import _update_application_token,_get_token_lifespan,_get_active_token,create_connection,close_connection
from conn.electronic_cash_configs import outh_params,register_url_params

logger = logging.getLogger()

db_conn = create_connection()

"""
-.get current token lifesspan.
"""
token_lifespan = _get_token_lifespan(db_conn)[0].get('expireTime')
"""
-.api type
"""
API_TYPE = "production";
"""
-.have we exhausted the lifespan?
"""
if(token_lifespan >= int(outh_params['token_lifespan'])):
	"""
	-.request for a token.
	"""
	issued_token = oauth_generate_token(outh_params['consumer_key'],outh_params['consumer_secret'])
	
	"""
	-.get an instance of the class.
	"""
	if(issued_token is not None):
		mpesa = Mpesa(issued_token['access_token'],API_TYPE)
		"""
		-.build a dict of expected params i.e. ShortCode,ResponseType,ConfirmationURL,ValidationURL
		"""	
		data = {"ShortCode":register_url_params['short_code'],"ResponseType":register_url_params['response_type'],"ConfirmationURL":register_url_params['confirmation_url'],"ValidationURL":register_url_params['validation_url']}
		"""
		-.register callback url.
		"""	
		response = mpesa.c2b_register_url(data)
		"""
		-.update consumer app token.
		"""		
		if(issued_token['access_token'] is not None):
			response_b = _update_application_token(db_conn,issued_token['access_token'],outh_params['consumer_key'],outh_params['consumer_secret'])
		
		print(response)		
	else:
		print("Failed to Access Token.")		
else:
	"""
	-.read active token.
	"""
	active_token = _get_active_token(db_conn)[0].get('activeToken')
	"""
	-.get an instance of the class.
	"""
	mpesa = Mpesa(active_token,API_TYPE)	
	"""
	-.build a dict of expected params i.e. ShortCode,Amount,Msisdn,BillRefNumber.
	"""		
	data = {"ShortCode":register_url_params['short_code'],"Amount":"9815","Msisdn":"254708374149","BillRefNumber":register_url_params['short_code']}
	
	response = mpesa.c2b_simulate_transaction(data)
	
	logging.info(data)
	#response = "Ok"
	print(response)
