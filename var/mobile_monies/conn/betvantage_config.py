#!/usr/bin/python

import logging
import ConfigParser
import os

"""
current_dir = os.getcwd()
CONFIG_FILE = current_dir + '\config\electronic_cash.conf'
"""

current_dir = os.path.join("D:/", "mobile_monies")

CONFIG_FILE = current_dir + '\\conn\\betvantage_config.conf'

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SMS_HANDLER")
logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
hdlr = logging.FileHandler(config.get("logger", "log_file"))
hdlr = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

host   = config.get("mysql", "host")
port   = config.get("mysql", "port")
user   = config.get("mysql", "user")
passwd = config.get("mysql", "password")
db     = config.get("mysql", "database")
connection_timeout = config.get("mysql", "connection_timeout")
mysql_params = {'host':host, 'port':port, 'user':user, 'passwd':passwd, 'db':db, 'connection_timeout':connection_timeout}

consumer_key = config.get("outh","consumer_key")
consumer_secret = config.get("outh","consumer_secret")
token_lifespan = config.get("outh","token_lifespan")
outh_params = {'consumer_key':consumer_key, 'consumer_secret':consumer_secret, 'token_lifespan':token_lifespan}

short_code       = config.get("sms","short_code")
balance_keyword  = config.get("sms","balance")
register_keyword = config.get("sms","register")
withdraw_keyword = config.get("sms","withdraw")
stop_keyword     = config.get("sms","stop")
hash_delimiter   = config.get("sms","hashtag")

sms_params = {'short_code':short_code,'balance':balance_keyword,'register':register_keyword,'withdraw':withdraw_keyword,'stop':stop_keyword,'hash_delimiter':hash_delimiter}

minimum_amount = config.get("game","minimum_amount")
maximum_amount = config.get("game","maximum_amount")
mpesa_charge   = config.get("game","mpesa_charge")
airtel_charge  = config.get("game","airtel_charge")
telkom_charge  = config.get("game","telkom_charge")
equitel_charge = config.get("game","equitel_charge")
register_bonus = config.get("game","register_bonus")
stake_command  = config.get("game","stake_command")
paybill_number = config.get("game","paybill_number")
cost_per_bet   = config.get("game","cost_per_bet")
minimum_bonus  = config.get("game","minimum_bonus")

game_params = {'min_withdrawal_amount':minimum_amount,'max_withdrawal_amount':maximum_amount,'mpesa_charge':mpesa_charge,'airtel_charge':airtel_charge,'telkom_charge':telkom_charge,'equitel_charge':equitel_charge,'register_bonus':register_bonus,'stake_command':stake_command,'paybill_number':paybill_number,'cost_per_bet':cost_per_bet,'minimum_bonus':minimum_bonus}

code   = config.get("prefix","code")
safcom = config.get("prefix","safcom")
airtel = config.get("prefix","airtel")
telkom = config.get("prefix","telkom")

prefix_params = {'code':code,'safcom':safcom,'airtel':airtel,'telkom':telkom}
