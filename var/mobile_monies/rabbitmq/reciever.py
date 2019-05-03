#!/usr/bin/python

import sys
import pika
import time
import json

from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from conn.dbhelper import _record_live_mpesa_transaction_log,create_connection,close_connection

db_conn = create_connection()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs5',exchange_type='fanout',durable=True)

result = channel.queue_declare(exclusive=True,durable=True)

queue_name = result.method.queue

size = result.method.message_count == 0

channel.queue_bind(exchange='logs5',queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print " [x] Received %r" % (body,)
	_record_live_mpesa_transaction_log(db_conn,json.loads(body))
	time.sleep( body.count('.') )
	print " [x] Done"
	ch.basic_ack(delivery_tag = method.delivery_tag)
	

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,queue=queue_name)

channel.start_consuming()