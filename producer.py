#!/usr/bin/env python
import os
import sys
import base64
import cv2
import json
import numpy as np
from random import choice
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Producer

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    # Create Producer instance
    print(f"producer config:{config}")
    producer = Producer(config)

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    # Produce data by selecting random values from these lists.
    topic = "purchases_"
    img_path="./org_data/"
    img_list=[file for file in os.listdir(img_path)]

    #TODO Read Json
    DATA={}
    DATA["moduleData"] = {}
    for file in img_list:
        image_base64 = None
        with open(f"{img_path}{file}", 'rb') as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        print(f"image_base64:{len(image_base64)}")
        DATA = {
            'image': image_base64,
            'metadata': {
                'name': file ,
                'format': 'jpeg'
            }
        }
        MD = json.dumps(DATA)
        producer.produce(topic, json.dumps(MD).encode('utf-8'), callback=delivery_callback)

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()
