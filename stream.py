import mastodon
from mastodon import Mastodon
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from kafka import KafkaProducer
import socket
import websocket, base64, json
import pulsar
from pulsar.schema import *
import paho.mqtt.client as mqtt
import time
import sys
import datetime
import subprocess
import sys
import os
from subprocess import PIPE, Popen
import traceback
import math
import base64
import json
from time import gmtime, strftime
import random, string
import psutil
import base64
import uuid
import json
import socket 
import logging
from jsonpath_ng import jsonpath, parse
import re

#### https://github.com/tspannhw/FLiP-PulsarDevPython101/

#### MQTT
client = mqtt.Client("mastodon-producer")
client.connect("localhost", 1883, 180)
# client.publish("persistent://public/default/mqtt-2", payload=json_string, qos=0, retain=True)

#### Apache Pulsar

pulsarClient = pulsar.Client('pulsar://localhost:6650')


#### AMQP/RabbitMQ
#parms = pika.URLParameters('amqp://localhost:5672/')
#connection = pika.BlockingConnection(parms)
#channel = connection.channel()

#try:
#    channel.queue_declare("amqp-enviro")
#    channel.basic_publish(exchange="", routing_key="amqp-enviro", body=json_string.encode('utf-8'))
#finally:
#    connection.close()

#### Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092',retries=3)
#producer.send('rp4-kafka-1', json.dumps(row).encode('utf-8'))


class mastodondata(Record):
    language = String()
    created_at = String()
    ts = Float()
    uuid = String()
    uri = String()
    url = String()
    favourites_count = Integer()
    replies_count = Integer()
    reblogs_count = Integer()
    content = String()
    username = String()
    accountname = String()
    displayname = String()
    note = String()
    followers_count = Integer()
    statuses_count = Integer()


keywordList = ['apache spark','Apache Spark', 'Apache Pinot','flink','Flink','Apache Flink','kafka', 'Kafka', 'Apache Kafka', 'pulsar', 'Pulsar', 'datapipeline', 'real-time', 'real-time streaming', 'StreamNative', 'Confluent', 'RedPandaData', 'Apache Pulsar', 'streaming', 'Streaming', 'big data', 'Big Data']

words_re = re.compile("|".join(keywordList))

class Listener(mastodon.StreamListener):

    def on_update(self, status):
        if words_re.search(status.content):
            pulsarProducer = pulsarClient.create_producer(topic='persistent://public/default/mastodon',
                schema=JsonSchema(mastodondata), properties={"producer-name": "mastodon-py-strean","producer-id": "mastodon-producer" })
            mastodonRec = mastodondata()
            uuid_key = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S",gmtime()),uuid.uuid4())
            mastodonRec.language = status.language
            mastodonRec.created_at = str(status.created_at)
            mastodonRec.ts = float(strftime("%Y%m%d%H%M%S",gmtime()))
            mastodonRec.uuid = uuid_key
            mastodonRec.uri = status.uri
            mastodonRec.url = status.url
            mastodonRec.favourites_count = status.favourites_count
            mastodonRec.replies_count = status.replies_count
            mastodonRec.reblogs_count = status.reblogs_count
            mastodonRec.content = status.content 
            mastodonRec.username = status.account.username
            mastodonRec.accountname = status.account.acct
            mastodonRec.displayname = status.account.display_name
            mastodonRec.note = status.account.note
            mastodonRec.followers_count = status.account.followers_count
            mastodonRec.statuses_count = status.account.statuses_count
            print(mastodonRec.ts)
            pulsarProducer.send(mastodonRec,partition_key=str(uuid_key))
            pulsarProducer.flush()
            #producer.send('rp4-kafka-1', mastodonRec.encode('utf-8'))
            #producer.flush()

    def on_notification(self, notification):
        # print(f"on_notification: {notification}")
        print("notification")

# Register your app! This only needs to be done once (per server, or when
# distributing rather than hosting an application, most likely per device and server).
# Uncomment the code and substitute in your information:
Mastodon.create_app(
    'streamreader',
    api_base_url = 'https://mastodon.social'
)

mastodon = Mastodon(api_base_url='https://mastodon.social')

# read https://mastodon.social/api/v1/streaming/public
#mastodon.stream_public(listener, run_async=False, timeout=300, reconnect_async=False, reconnect_async_wait_sec=5)

mastodon.stream_public(Listener())
