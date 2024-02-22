#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# A simple example demonstrating use of AvroDeserializer.

import argparse
import base64
import cv2
import numpy as np
import os

from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

class Image(object):
    """
    User record

    Args:
        name (str): frame's name

        image_base64 (string): image_base_64

        channel (int): no. of channel in image

        image height (int): image height

        image width (int): image width
    """

    def __init__(self, frame_name, channel, img_ht, img_wd, img_base64):
        self.frame_name = frame_name
        self.channel = channel
        self.img_ht = img_ht
        self.img_wd = img_wd
        self.img_base64 = img_base64


def image_to_dict(image, ctx):
    """
    Returns a dict representation of a User instance for serialization.

    Args:
        image (Image): Image instance.

        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.

    Returns:
        dict: Dict populated with user attributes to be serialized.
    """

    # User._address must not be serialized; omit from dict
    if image is None:
        return None
    return Image(frame_name=image['frame_name'],
                img_base64=image['img_base64'],
                img_ht=image['img_ht'],
                img_wd=image['img_wd'],
                channel=image['channel'])


def dict_to_user(obj, ctx):
    """
    Converts object literal(dict) to a User instance.

    Args:
        obj (dict): Object literal(dict)

        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.
    """

    if obj is None:
        return None

    return User(name=obj['name'],
                favorite_number=obj['favorite_number'],
                favorite_color=obj['favorite_color'])


def main(args):
    topic = args.topic
    schema = args.schema

    #path = os.path.realpath(os.path.dirname(__file__))
    with open(f"{schema}") as f:
        schema_str = f.read()

    schema_registry_conf = {'url': args.schema_registry}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    avro_deserializer = AvroDeserializer(schema_registry_client,
                                     schema_str,
                                     image_to_dict)


    consumer_conf = {'bootstrap.servers': args.bootstrap_servers,
                     'group.id': args.group,
                     'auto.offset.reset': "earliest"}

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            if msg is None or msg.key() is None:
                continue
            print(f"msg: {msg.key()}")
            image = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
            if image is not None:
                print("User record {}: frame_name: {}\n"
                      "\timage ht: {}\n"
                      "\timage width: {}\n"
                      .format(msg.key(), image.frame_name,
                              image.img_ht,
                              image.img_wd))
                # Decode the Base64 string back to bytes
                image_bytes = base64.b64decode(image.img_base64)
                # Convert the bytes to a numpy array
                image_np = np.frombuffer(image_bytes, dtype=np.uint8)
                # Decode the numpy array to a CV2 image
                cv_image = cv2.imdecode(image_np, flags=cv2.IMREAD_COLOR)
                cv2.imwrite(f"./from_receiver_2/{image.frame_name}", cv_image)
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AvroDeserializer example")
    parser.add_argument('-b', dest="bootstrap_servers", required=True,
                        help="Bootstrap broker(s) (host[:port])")
    parser.add_argument('-s', dest="schema_registry", required=True,
                        help="Schema Registry (http(s)://host[:port]")
    parser.add_argument('-j', dest="schema", required=True,
                        help="Schema Json")
    parser.add_argument('-t', dest="topic", default="example_serde_avro",
                        help="Topic name")
    parser.add_argument('-g', dest="group", default="example_serde_avro",
                        help="Consumer group")
    parser.add_argument('-p', dest="specific", default="true",
                        help="Avro specific record")

    main(parser.parse_args())
