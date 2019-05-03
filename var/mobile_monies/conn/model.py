#!/usr/bin/python

"""
developer skype: alec_host
"""

import time
import signal
import sys
import eventlet
import logging

from decimal import Decimal
from datetime import datetime

from dbhelper import _read_incoming_sms_db,_sms_queue_cnt_db,_processed_inbound_sms_db,_register_on_sms_db,_queue_outgoing_sms_db,_verify_customer_db,_withdraw_cash_db,_place_bet_db,_sync_bonus_db
from betvantage_config import logger,sms_params,game_params,prefix_params
from messageTemplate.list import *

eventlet.monkey_patch()

"""
#-.routine to process sms.
"""
def _process_sms(q,connection):
	"""
	get count of the queue. 	
	"""
	heap_size = _sms_queue_cnt_db(connection)	
	if(heap_size > 0):
		record_id = ""
		default   = "'0'"
		timestamp = datetime.now().strftime('%d/%m/%y')+" at "+datetime.now().strftime('%I:%M %p')
		"""
		routine call to read inbound sms.
		"""
		sms_tuple = _read_incoming_sms_db(connection)
		"""
		loop thro' records in a tuple.
		"""							
		for var in sms_tuple:
		
			message = var['Message'].strip().lower()
			"""
			get a list of comma delimited record ids.
			"""
			record_id = (record_id + "," + "'" + str(var['ID']) + "'")
			"""
			user authentication & info.
			"""
			client_found = _verify_customer_db(var['MSISDN'],'0',connection)
			"""
			routine call to identify msisdn's op network.
			"""
			operator_info = _get_operator_network(var['MSISDN'][3:])
			"""
			-
			"""
			if(client_found[0] == "1"):
				"""
				get client information in format .i.e [FirstName|Language|PromotionNotificationFlag|Balance|Bonus|StakeCountTracker]
				"""	
				client_information = client_found[1].split(',')
				"""
				match inbound message to keyword list.
				"""
				if(message in sms_params['balance']):
					"""
					format message.
					"""
					if(client_information[1] == "en"):
						_sms = TPL_BALANCE[0].replace("{0}",client_information[0]).replace("{1}",client_information[3]).replace("{2}",timestamp)
					else:
						_sms = TPL_BALANCE[1].replace("{0}",client_information[0]).replace("{1}",client_information[3]).replace("{2}",timestamp)
				elif(message in sms_params['register']):
					"""
					format message. operator_info[1] ~ pay bill code.
					"""
					if(client_information[1] == "en"):
						_sms = TPL_REGISTRATION[0].replace("{0}",operator_info[1]).replace("{1}",timestamp)
					else:
						_sms = TPL_REGISTRATION[1].replace("{0}",operator_info[1]).replace("{1}",timestamp)				
					"""
					routine call to register new customer.
					"""
					q.put(_register_on_sms_db(var['MSISDN'],connection))
				elif(message in sms_params['stop']):
					"""
					format message.
					"""
					if(client_information[1] == "en"):
						_sms = TPL_STOP[0].replace("{0}",client_information[0]).replace("{1}",timestamp)	
					else:
						_sms = TPL_STOP[1].replace("{0}",client_information[0]).replace("{1}",timestamp)	
					"""
					stop notification call.
					"""			
				else:
					"""
					check if message has a # symbol.
					"""
					if(sms_params['hash_delimiter'] in message):
						"""
						explode text.
						"""
						sms_action = message.split('#')
						"""
						read text action.
						"""
						if(sms_action[0] in sms_params['withdraw']):
							"""
							check available balance.
							"""
							if(int(float(client_information[3])) >= int(sms_action[1])):
								"""
								command w#amount.
								"""
								if(int(sms_action[1]) >= int(game_params['min_withdrawal_amount']) and int(sms_action[1]) < int(game_params['max_withdrawal_amount'])):
									"""
									routine to calc fee on withdrawal. operator_info[0] ~ network identity
									"""
									fee = _calc_withdrawal_fee(sms_action[1],operator_info[0])
									"""
									compute current balance.
									"""
									current_balance = Decimal(client_information[3]) - (int(fee) + int(sms_action[1]))
									"""
									current_balance is not -ve.
									"""
									if(current_balance >= 0):
										"""
										update wallet balance.
										"""
										q.put(_withdraw_cash_db(var['MSISDN'],(int(fee) + int(sms_action[1])),connection))
										"""
										format message.
										"""
										if(client_information[1] == "en"):
											_sms = TPL_WITHDRAW[0].replace("{0}",client_information[0]).replace("{1}",sms_action[1]).replace("{2}",str(current_balance))
										else:
											_sms = TPL_WITHDRAW[1].replace("{0}",client_information[0]).replace("{1}",sms_action[1]).replace("{2}",str(current_balance))
									else:
										"""
										format message.
										"""
										if(client_information[1] == "en"):
											_sms = TPL_INSUFFICIENT[0].replace("{0}",client_information[0]).replace("{1}",client_information[3])
										else:
											_sms = TPL_INSUFFICIENT[1].replace("{0}",client_information[0]).replace("{1}",client_information[3])	
								elif(int(sms_action[1]) >= int(game_params['max_withdrawal_amount'])):
									"""
									format message.
									"""
									if(client_information[1] == "en"):
										_sms = TPL_WITHDRAW_MAX[0].replace("{0}",client_information[0]).replace("{1}",game_params['max_withdrawal_amount'])
									else:
										_sms = TPL_WITHDRAW_MAX[1].replace("{0}",client_information[0]).replace("{1}",game_params['max_withdrawal_amount'])							
								else:
									"""
									format message.
									"""
									if(client_information[1] == "en"):
										_sms = TPL_WITHDRAW_MIN[0].replace("{0}",client_information[0]).replace("{1}",game_params['min_withdrawal_amount'])
									else:
										_sms = TPL_WITHDRAW_MIN[1].replace("{0}",client_information[0]).replace("{1}",game_params['min_withdrawal_amount'])	
							else:
								"""
								format message.
								"""
								if(client_information[1] == "en"):
									_sms = TPL_INSUFFICIENT[0].replace("{0}",client_information[0]).replace("{1}",client_information[3])
								else:
									_sms = TPL_INSUFFICIENT[1].replace("{0}",client_information[0]).replace("{1}",client_information[3])
						else:
							"""
							remove white spaces & make all caps.
							"""
							stake = message.strip().upper()
							"""
							match item in two lists.
							"""
							if(set(stake.split('#')).intersection(game_params['stake_command'])):
								"""
								reverse the sms.
								"""
								reverse_string = stake[::-1]
								"""
								get bet amount .
								"""
								bet_amount = reverse_string.split('#')[0][::-1]
								"""
								check if client has bonus.
								""" 
								if(int(float(client_information[4])) > 0):
									print("bonus has to be exhausted")
									_sync_bonus_db(var['MSISDN'],bonus,connection);
									_sms = "we have bonus credit"
								else:
									"""
									verify bet amount staked.
									"""
									if(int(bet_amount) >= int(game_params['cost_per_bet'])):
										"""
										verify client has enough a/c balance.
										"""
										if(int(float(client_information[3])) >= int(bet_amount)):
											"""
											format message.
											"""
											if(client_information[1] == "en"):
												_sms = TPL_SUCCESS_BET[0].replace("{0}",client_information[0]).replace("{1}",stake.upper()).replace("{2}",timestamp)
											else:
												_sms = TPL_SUCCESS_BET[1].replace("{0}",client_information[0]).replace("{1}",stake.upper()).replace("{2}",timestamp)
											"""
											routine call to update a/c balance.
											"""
											q.put(_place_bet_db(var['MSISDN'],bet_amount,connection))
										else:
											"""
											format message.
											"""
											if(client_information[1] == "en"):
												_sms = TPL_INSUFFICIENT[0].replace("{0}",client_information[0]).replace("{1}",client_information[3]).replace("{2}",timestamp)
											else:
												_sms = TPL_INSUFFICIENT[1].replace("{0}",client_information[0]).replace("{1}",client_information[3]).replace("{2}",timestamp)
									else:
										"""
										format message.
										"""
										if(client_information[1] == "en"):
											_sms = TPL_STAKE_AMOUNT[0].replace("{0}",client_information[0]).replace("{1}",game_params['cost_per_bet']).replace("{2}",timestamp)
										else:
											_sms = TPL_STAKE_AMOUNT[1].replace("{0}",client_information[0]).replace("{1}",game_params['cost_per_bet']).replace("{2}",timestamp)									
							else:
								"""
								format message.
								"""
								if(client_information[1] == "en"):
									_sms = TPL_INVALID_BET[0].replace("{0}",client_information[0]).replace("{1}",stake.upper()).replace("{2}",timestamp)
								else:
									_sms = TPL_INVALID_BET[1].replace("{0}",client_information[0]).replace("{1}",stake.upper()).replace("{2}",timestamp)
					else:					
						"""
						write to miscellaneous.
						"""
						print('miscellaneous')
				"""
				push an sms notification.
				"""	
				q.put(_queue_outgoing_sms_db(var['MSISDN'],sms_params['short_code'],_sms,connection))	
				"""
				show activity.
				"""
				#print("...")
			else:
				"""
				push an sms notification.
				"""	
				q.put(_queue_outgoing_sms_db(var['MSISDN'],sms_params['short_code'],"Invalid PIN",connection))
			
		"""
		get a safe list of record IDs.
		"""	
		Ids = (default+record_id)		
		"""
		routine call :- mark record[s] as processed.
		"""	
		q.put(_processed_inbound_sms_db(Ids,connection))
	
"""
#-.routine compute withdrawal fees.
"""
def _calc_withdrawal_fee(withdraw_amount,network_identity):
	if(network_identity == "SAF"):
		if(int(withdraw_amount) >= int(game_params['min_withdrawal_amount']) and int(withdraw_amount) <= int(game_params['mpesa_charge'].split(',')[0].split('-')[1])):
			charge = game_params['mpesa_charge'].split(',')[0].split('-')[2]
		elif(int(withdraw_amount) >= int(game_params['mpesa_charge'].split(',')[1].split('-')[1])):
			charge = game_params['mpesa_charge'].split(',')[1].split('-')[2]
		else:
			charge = 0
	elif(network_identity == "AIR"):
		charge = 0
	elif(network_identity == "TLM"):
		charge = 0
	elif(network_identity == "EQL"):
		charge = 0

	return charge
"""
#-.routine identify msisdn network.
"""	
def _get_operator_network(msisdn):
	client_mobile = msisdn
	if(client_mobile[0:3] in prefix_params['safcom']):
		network_identity  = "SAF"
		pay_bill_code = game_params['paybill_number'].split(',')[0]
	elif(client_mobile[0:3] in prefix_params['airtel']):
		network_identity = "AIR"
		pay_bill_code = game_params['paybill_number'].split(',')[1]
	elif(client_mobile[0:3] in prefix_params['telkom']):
		network_identity = "TLM"
		pay_bill_code = game_params['paybill_number'].split(',')[2]
	else:
		network_identity = "EQL"
		pay_bill_code = game_params['paybill_number'].split(',')[3]
		
	return [network_identity,pay_bill_code]	

