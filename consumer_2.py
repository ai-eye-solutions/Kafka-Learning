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
    topic = "purchases_"
    consumer.subscribe([topic], on_assign=reset_offset)

    # Poll for new messages from Kafka and print them.
    #create dir for receiver_1
    if not os.path.exists("./from_receiver_2/"):
        os.mkdir("./from_receiver_2/")
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
                file_name = message_data['metadata']['name']
                print(f"length of img_data: {len(img_data)}")
                # Handle image or metadata as required
                print("Received image:", message_data['metadata']['name'])
                # Extract the (optional) key and value, and print.
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
                img_matlab = cv2.putText(image, 'from Receiver_2', org, font,
                               fontScale, color, thickness, cv2.LINE_AA)
                cv2.imwrite(f"./from_receiver_2/{file_name}", image)
                
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
