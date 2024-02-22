#!/usr/bin/env python
import base64
import cv2
import json
import numpy as np
import os
import sys
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING
from confluent_kafka import Producer

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    #TODO Intialize producer_2 instance
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
    config.update(config_parser['consumer'])

    # Create Consumer instance
    print(f"consumer: {config}")
    consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # Subscribe to topic
    topic = "purchases"
    consumer.subscribe([topic], on_assign=reset_offset)

    # Poll for new messages from Kafka and print them.
    #create dir for receiver_1
    if not os.path.exists("./from_receiver/"):
        os.mkdir("./from_receiver/")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                print(f"msg:{msg}")
                message_data = json.loads(json.loads(msg.value().decode('utf-8')))
                image_base64 = message_data['image']
                img_data = base64.b64decode(image_base64)
                nparr = np.frombuffer(img_data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                # font
                font = cv2.FONT_HERSHEY_SIMPLEX
                # org
                org = (1080, 50)
                # fontScale
                fontScale = 1
                # Blue color in BGR
                color = (255, 0, 0)
                # Line thickness of 2 px
                thickness = 2
                # Using cv2.putText() method
                img_matlab = cv2.putText(image, 'from Receiver', org, font,
                               fontScale, color, thickness, cv2.LINE_AA)
                file_name = message_data['metadata']['name']
                print(f"length of img_data: {len(img_data)}")
                # Handle image or metadata as required
                print("Received image:", message_data['metadata']['name'])
                # Extract the (optional) key and value, and print.
                cv2.imwrite(f"./from_receiver/{file_name}", img_matlab)

                #TODO Send this data to receiver_2
                DATA={}
                DATA["moduleData"] = {}
                #image_base64 = base64.b64encode(img_matlab)#.decode('utf-8'))
                print(f"image_base64:{len(image_base64)}")
                DATA = {
                    'image': image_base64,
                    'metadata': {
                        'name': file_name ,
                        'format': 'jpeg'
                    }
                }
                topic = "purchases_"
                MD = json.dumps(DATA)
                #START = time.time()*1000
                producer.produce(topic, json.dumps(MD).encode('utf-8'), callback=delivery_callback)
                print(f"message sent to receiver_2 !!") 
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
