#!/usr/bin/python

"""
"""
import os
import json
import logging

import requests

from conn.dbhelper import _record_live_mpesa_transaction_log,create_connection,close_connection

logger = logging.getLogger()

db_conn = create_connection()

body = {"MSISDN":"2547322223","TransID":"CVSBERRTY","TransAmount":"10","FirstName":"Joe","MiddleName":"Doe","LastName":"Kite","TransTime":"2018-09-17 00:00:00","BusinessShortCode":"612037","BillRefNumber":"612037","InvoiceNumber":"123456","OrgAccountBalance":"1200","ThirdPartyTransID":"123456"}

print body

_record_live_mpesa_transaction_log(db_conn,body)
requests.packages.urllib3.disable_warnings()
#-.https://197.254.25.230:6060/
resp = requests.get("https://474fcd4a.ngrok.io/MQ/publisher.php",verify = False)

print(resp)
