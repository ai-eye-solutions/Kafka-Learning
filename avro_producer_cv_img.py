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


# A simple example demonstrating use of AvroSerializer.

import argparse
import base64
import cv2
import io
import numpy as np
import os
from uuid import uuid4

from six.moves import input

from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

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
        user (User): User instance.

        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.

    Returns:
        dict: Dict populated with user attributes to be serialized.
    """

    # User._address must not be serialized; omit from dict
    return dict(frame_name=image.frame_name,
                img_base64=image.img_base64,
                img_ht=image.img_ht,
                img_wd=image.img_wd,
                channel=image.channel)


def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.

        msg (Message): The message that was produced or failed.

    Note:
        In the delivery report callback the Message.key() and Message.value()
        will be the binary format as encoded by any configured Serializers and
        not the same object that was passed to produce().
        If you wish to pass the original object(s) for key and value to delivery
        report callback we recommend a bound callback or lambda where you pass
        the objects along.
    """

    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


def main(args):
    topic = args.topic
    schema = args.schema

    #path = os.path.realpath(os.path.dirname(__file__))
    with open(f"{schema}") as f:
        schema_str = f.read()

    schema_registry_conf = {'url': args.schema_registry}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    avro_serializer = AvroSerializer(schema_registry_client,
                                     schema_str,
                                     image_to_dict)

    string_serializer = StringSerializer('utf_8')

    producer_conf = {'bootstrap.servers': args.bootstrap_servers}

    producer = Producer(producer_conf)

    print("Producing user records to topic {}. ^C to exit.".format(topic))
    img_path="./org_data/"
    img_list=[file for file in os.listdir(img_path)]
    count=0
    while count < len(img_list):
        # Serve on_delivery callbacks from previous calls to produce()
        producer.poll(0.0)
        try:
            image_base64 = None
            cv_img=cv2.imread(f"{img_path}{img_list[count]}")
            print(f"image shape: {cv_img.shape}")
            ht, wd, ch = cv_img.shape
            # Convert the image to bytes
            image_bytes = cv2.imencode('.jpg', cv_img)[1].tobytes()
            # Encode the image bytes as Base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            print(f"image_base64:{len(image_base64)}")
            print(f"image_base64:{type(image_base64)}")
            user = Image(frame_name=img_list[count],\
                         channel=ch,\
                         img_ht=ht,\
                         img_wd=wd,\
                         img_base64=image_base64\
                         )
            producer.produce(topic=topic,
                             key=string_serializer(str(uuid4())),
                             value=avro_serializer(user, SerializationContext(topic, MessageField.VALUE)),
                             on_delivery=delivery_report)
            count+=1
        except KeyboardInterrupt:
            break
        except ValueError:
            print("Invalid input, discarding record...")
            continue

    print("\nFlushing records...")
    producer.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AvroSerializer example")
    parser.add_argument('-b', dest="bootstrap_servers", required=True,
                        help="Bootstrap broker(s) (host[:port])")
    parser.add_argument('-s', dest="schema_registry", required=True,
                        help="Schema Registry (http(s)://host[:port]")
    parser.add_argument('-j', dest="schema", required=True,
                        help="Schema Json")
    parser.add_argument('-t', dest="topic", default="example_serde_avro",
                        help="Topic name")

    main(parser.parse_args())
