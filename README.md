# Kafka-Data-Transmission
This branch demonstrates the Key Concepts of a Schema Registry in kafka's producer and consumer, you can refer this [article](https://developer.confluent.io/courses/schema-registry/key-concepts/#:~:text=The%20schema%20registry%20is%20a,to%20and%20received%20from%20Kafka.)

## Below image explains how schema registry works
![image](https://github.com/safeproai/Kafka-Data-Trasmission/assets/141702049/d5b20215-345e-44a8-b142-42ce1c93277e)

## There are three following way we are using producer and consumer using different schema:
1. Normal data like (name, address, favorite number and color)
2. Produce and consume image data.
3. Running producer and consumer in seperate docker container with same docker-compose docker network.

# Steps to run the demo1:

## TO run demo with normal data follow below steps:
1. We will have to run `docker-compose -f docker-compose-kafka-setup.yml up -d`.
2. Register the schema for demo1 by running this python file `avro_schema_register_demo1.py`, this will register this usecase's schema
3. After that you can start producer in on terminal and consumer in other terminal.
   ## Producer terminal
   ```
   (env) nitin@nitin-safepro:~/Safepro/Workspace/ITMS_Phase2/Kafka-Data-Trasmission$ python avro_producer.py -b localhost:9092 -s http://0.0.0.0:8081 -t topic1 
   Producing user records to topic topic1. ^C to exit.
   Enter name: Ramesh
   Enter address: Delhi
   Enter favorite number: 1115
   Enter favorite color: black
   Enter name: Suresh
   Enter address: Mumbai 
   Enter favorite number: 0786
   Enter favorite color: red
   User record b'1b6f835e-c1a5-440a-b93d-9aba353dbde8' successfully produced to topic1 [0] at offset 0
   Enter name: ^C
   Flushing records...
   User record b'4bf85bfd-262d-4322-8255-7e2150657a24' successfully produced to topic1 [0] at offset 1
   ```
   ## Consumer Terminal
   ```
   (env) nitin@nitin-safepro:~/Safepro/Workspace/ITMS_Phase2/Kafka-Data-Trasmission$ python avro_consumer.py -b localhost:9092 -s http://0.0.0.0:8081 -t topic1
   msg: b'1b6f835e-c1a5-440a-b93d-9aba353dbde8'
   User record b'1b6f835e-c1a5-440a-b93d-9aba353dbde8': name: Ramesh
	 favorite_number: 1115
	 favorite_color: black

   msg: b'4bf85bfd-262d-4322-8255-7e2150657a24'
   User record b'4bf85bfd-262d-4322-8255-7e2150657a24': name: Suresh
	 favorite_number: 786
	 favorite_color: red

   ```
## TO run demo2 with image data follow below steps:
1. Down the `docker-compose -f docker-compose-kafka-setup.yml down` and start again `docker-compose -f docker-compose-kafka-setup.yml up -d`.
2. After that register schema to process imgage data by running `python avro_schema_register_demo2.py`
3. After that you can start producer in on terminal and consumer in other terminal.
   
   ## Producer terminal
```
(env) nitin@nitin-safepro:~/Safepro/Workspace/ITMS_Phase2/Kafka-Data-Trasmission$ python avro_producer_cv_img.py -b localhost:9092 -s http://0.0.0.0:8081 -t topic1 -j avro/image.avsc
Producing user records to topic topic1. ^C to exit.
image shape: (1080, 1920, 3)
image_base64:643828
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:744924
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:737840
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:774836
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:707012
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:700684
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:739080
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:723176
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:777272
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:743976
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:729500
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:757916
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:768908
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:718572
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:734992
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:733332
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:729144
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:708036
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:673000
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:779416
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:811008
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:718552
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:764952
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:685144
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:729684
image_base64:<class 'str'>
image shape: (1080, 1920, 3)
image_base64:712756
image_base64:<class 'str'>

Flushing records...
User record b'7bb257e4-fefb-44c2-912e-263c2fcb86d5' successfully produced to topic1 [0] at offset 0
User record b'f1911df7-5ea3-4ef9-8fd6-96787455dfc7' successfully produced to topic1 [0] at offset 1
User record b'9e41f068-2a0b-433a-81bc-2f976689caf0' successfully produced to topic1 [0] at offset 2
User record b'155ed0e4-ac42-4cfa-8ddf-904f1052aae1' successfully produced to topic1 [0] at offset 3
User record b'9236143c-2ee4-4fbb-a711-3d35e97c6082' successfully produced to topic1 [0] at offset 4
User record b'8335ab11-bb8e-4f7d-849b-4b2fdc503365' successfully produced to topic1 [0] at offset 5
User record b'588a11d1-7cfb-4d13-ad65-6f4c2c0ddb40' successfully produced to topic1 [0] at offset 6
User record b'7f5ce770-4173-4eef-9297-394cce4dd8a6' successfully produced to topic1 [0] at offset 7
User record b'28f36b14-14e6-4bec-83f2-59cfe5615e9d' successfully produced to topic1 [0] at offset 8
User record b'7c7f25a5-b533-466f-9948-ba528ae7382e' successfully produced to topic1 [0] at offset 9
User record b'd7c5f7fd-7ff0-469c-84b7-d67da63c36ad' successfully produced to topic1 [0] at offset 10
User record b'fd7541f1-0cde-4e54-a579-523647cf2971' successfully produced to topic1 [0] at offset 11
User record b'76d81e3e-5269-45be-996b-52aa555bdec5' successfully produced to topic1 [0] at offset 12
User record b'2d748eed-b768-49e0-8a4a-dcd2f4555668' successfully produced to topic1 [0] at offset 13
User record b'da488b4c-d71b-4a8f-b1da-0a4a98702440' successfully produced to topic1 [0] at offset 14
User record b'd684b89f-8f0e-4e93-a741-e7471e407eab' successfully produced to topic1 [0] at offset 15
User record b'09e694d6-90b1-4b83-b287-3e6bd59fca10' successfully produced to topic1 [0] at offset 16
User record b'892c73d8-c9ed-4ccb-9119-3cbb1ad5d0f7' successfully produced to topic1 [0] at offset 17
User record b'5a2f43ed-72ea-4411-a978-b1d4e9bbc256' successfully produced to topic1 [0] at offset 18
User record b'e5ba312c-74da-4ea4-9b2c-76efaf546324' successfully produced to topic1 [0] at offset 19
User record b'060c8de3-0b1f-46b1-9c1a-638314e01ae6' successfully produced to topic1 [0] at offset 20
User record b'f3da18ee-1c5f-4f1b-822c-45d28726b13b' successfully produced to topic1 [0] at offset 21
User record b'91ab5e60-f72a-4a9d-9b9c-d20ce60deab6' successfully produced to topic1 [0] at offset 22
User record b'6cfc24a3-35eb-4c74-aaec-a1a4e5d51cfb' successfully produced to topic1 [0] at offset 23
User record b'49ce1c3f-2a6c-4190-9380-70ccb0935bba' successfully produced to topic1 [0] at offset 24
User record b'565ff31c-8b84-4191-9b8a-e39e8869485e' successfully produced to topic1 [0] at offset 25
(env) nitin@nitin-safepro:~/Safepro/Workspace/ITMS_Phase2/Kafka-Data-Trasmission$ 
```
   ## Consumer Terminal
```
(env) nitin@nitin-safepro:~/Safepro/Workspace/ITMS_Phase2/Kafka-Data-Trasmission$ python avro_consumer_cv_img.py -b localhost:9092 -s http://0.0.0.0:8081 -t topic1 -j avro/image.avsc
msg: b'7bb257e4-fefb-44c2-912e-263c2fcb86d5'
User record b'7bb257e4-fefb-44c2-912e-263c2fcb86d5': frame_name: 7th_Nov_data00005.jpg
	image ht: 1080
	image width: 1920

msg: b'f1911df7-5ea3-4ef9-8fd6-96787455dfc7'
User record b'f1911df7-5ea3-4ef9-8fd6-96787455dfc7': frame_name: 7th_Nov_data00002.jpg
	image ht: 1080
	image width: 1920

msg: b'9e41f068-2a0b-433a-81bc-2f976689caf0'
User record b'9e41f068-2a0b-433a-81bc-2f976689caf0': frame_name: 7th_Nov_data00010.jpg
	image ht: 1080
	image width: 1920

msg: b'155ed0e4-ac42-4cfa-8ddf-904f1052aae1'
User record b'155ed0e4-ac42-4cfa-8ddf-904f1052aae1': frame_name: 7th_Nov_data00023.jpg
	image ht: 1080
	image width: 1920

msg: b'9236143c-2ee4-4fbb-a711-3d35e97c6082'
User record b'9236143c-2ee4-4fbb-a711-3d35e97c6082': frame_name: 7th_Nov_data00012.jpg
	image ht: 1080
	image width: 1920

msg: b'8335ab11-bb8e-4f7d-849b-4b2fdc503365'
User record b'8335ab11-bb8e-4f7d-849b-4b2fdc503365': frame_name: 7th_Nov_data00020.jpg
	image ht: 1080
	image width: 1920

msg: b'588a11d1-7cfb-4d13-ad65-6f4c2c0ddb40'
User record b'588a11d1-7cfb-4d13-ad65-6f4c2c0ddb40': frame_name: 7th_Nov_data00000.jpg
	image ht: 1080
	image width: 1920

msg: b'7f5ce770-4173-4eef-9297-394cce4dd8a6'
User record b'7f5ce770-4173-4eef-9297-394cce4dd8a6': frame_name: 7th_Nov_data00017.jpg
	image ht: 1080
	image width: 1920

msg: b'28f36b14-14e6-4bec-83f2-59cfe5615e9d'
User record b'28f36b14-14e6-4bec-83f2-59cfe5615e9d': frame_name: 7th_Nov_data00018.jpg
	image ht: 1080
	image width: 1920

msg: b'7c7f25a5-b533-466f-9948-ba528ae7382e'
User record b'7c7f25a5-b533-466f-9948-ba528ae7382e': frame_name: 7th_Nov_data00001.jpg
	image ht: 1080
	image width: 1920

msg: b'd7c5f7fd-7ff0-469c-84b7-d67da63c36ad'
User record b'd7c5f7fd-7ff0-469c-84b7-d67da63c36ad': frame_name: 7th_Nov_data00004.jpg
	image ht: 1080
	image width: 1920

msg: b'fd7541f1-0cde-4e54-a579-523647cf2971'
User record b'fd7541f1-0cde-4e54-a579-523647cf2971': frame_name: 7th_Nov_data00021.jpg
	image ht: 1080
	image width: 1920

msg: b'76d81e3e-5269-45be-996b-52aa555bdec5'
User record b'76d81e3e-5269-45be-996b-52aa555bdec5': frame_name: 7th_Nov_data00024.jpg
	image ht: 1080
	image width: 1920

msg: b'2d748eed-b768-49e0-8a4a-dcd2f4555668'
User record b'2d748eed-b768-49e0-8a4a-dcd2f4555668': frame_name: 7th_Nov_data00007.jpg
	image ht: 1080
	image width: 1920

msg: b'da488b4c-d71b-4a8f-b1da-0a4a98702440'
User record b'da488b4c-d71b-4a8f-b1da-0a4a98702440': frame_name: 7th_Nov_data00008.jpg
	image ht: 1080
	image width: 1920

msg: b'd684b89f-8f0e-4e93-a741-e7471e407eab'
User record b'd684b89f-8f0e-4e93-a741-e7471e407eab': frame_name: 7th_Nov_data00013.jpg
	image ht: 1080
	image width: 1920

msg: b'09e694d6-90b1-4b83-b287-3e6bd59fca10'
User record b'09e694d6-90b1-4b83-b287-3e6bd59fca10': frame_name: 7th_Nov_data00011.jpg
	image ht: 1080
	image width: 1920

msg: b'892c73d8-c9ed-4ccb-9119-3cbb1ad5d0f7'
User record b'892c73d8-c9ed-4ccb-9119-3cbb1ad5d0f7': frame_name: 7th_Nov_data00003.jpg
	image ht: 1080
	image width: 1920

msg: b'5a2f43ed-72ea-4411-a978-b1d4e9bbc256'
User record b'5a2f43ed-72ea-4411-a978-b1d4e9bbc256': frame_name: 7th_Nov_data00014.jpg
	image ht: 1080
	image width: 1920

msg: b'e5ba312c-74da-4ea4-9b2c-76efaf546324'
User record b'e5ba312c-74da-4ea4-9b2c-76efaf546324': frame_name: 7th_Nov_data00025.jpg
	image ht: 1080
	image width: 1920

msg: b'060c8de3-0b1f-46b1-9c1a-638314e01ae6'
User record b'060c8de3-0b1f-46b1-9c1a-638314e01ae6': frame_name: 7th_Nov_data00019.jpg
	image ht: 1080
	image width: 1920

msg: b'f3da18ee-1c5f-4f1b-822c-45d28726b13b'
User record b'f3da18ee-1c5f-4f1b-822c-45d28726b13b': frame_name: 7th_Nov_data00009.jpg
	image ht: 1080
	image width: 1920

msg: b'91ab5e60-f72a-4a9d-9b9c-d20ce60deab6'
User record b'91ab5e60-f72a-4a9d-9b9c-d20ce60deab6': frame_name: 7th_Nov_data00022.jpg
	image ht: 1080
	image width: 1920

msg: b'6cfc24a3-35eb-4c74-aaec-a1a4e5d51cfb'
User record b'6cfc24a3-35eb-4c74-aaec-a1a4e5d51cfb': frame_name: 7th_Nov_data00006.jpg
	image ht: 1080
	image width: 1920

msg: b'49ce1c3f-2a6c-4190-9380-70ccb0935bba'
User record b'49ce1c3f-2a6c-4190-9380-70ccb0935bba': frame_name: 7th_Nov_data00016.jpg
	image ht: 1080
	image width: 1920

msg: b'565ff31c-8b84-4191-9b8a-e39e8869485e'
User record b'565ff31c-8b84-4191-9b8a-e39e8869485e': frame_name: 7th_Nov_data00015.jpg
	image ht: 1080
	image width: 1920

```

## TO run demo3 with image data follow below steps:
1. Down the `docker-compose -f docker-compose-kafka-setup.yml down` and start again `docker-compose -f docker-compose-kafka-setup-containers.yml up -d`.
2. After that register same demo2 schema to process imgage data by running `python avro_schema_register_demo2.py`
3. After that you can start producer in on terminal and consumer in other terminal.

    ## Producer terminal
```
(env) nitin@nitin-safepro:~/Safepro/Workspace/ITMS_Phase2/Kafka-Data-Trasmission$ python3 avro_consumer_cv_img.py -b broker:29092 -s http://10.16.239.5:8081 -t topic1 -j avro/image.avsc
Producing user records to topic topic1. ^C to exit.
image shape: (1080, 1920, 3)
image_base64:643828
image_base64:<class 'str'>
image shape: (1080, 1920, 3)

```

   ## Consumer Terminal
```
(env) nitin@nitin-safepro:~/Safepro/Workspace/ITMS_Phase2/Kafka-Data-Trasmission$ python avro_consumer_cv_img.py -b broker:29092 -s http://10.16.239.5:8081 -t topic1 -j avro/image.avsc
msg: b'7bb257e4-fefb-44c2-912e-263c2fcb86d5'
User record b'7bb257e4-fefb-44c2-912e-263c2fcb86d5': frame_name: 7th_Nov_data00005.jpg
	image ht: 1080
	image width: 1920

msg: b'f1911df7-5ea3-4ef9-8fd6-96787455dfc7'
User record b'f1911df7-5ea3-4ef9-8fd6-96787455dfc7': frame_name: 7th_Nov_data00002.jpg
	image ht: 1080
	image width: 1920

msg: b'9e41f068-2a0b-433a-81bc-2f976689caf0'
User record b'9e41f068-2a0b-433a-81bc-2f976689caf0': frame_name: 7th_Nov_data00010.jpg
	image ht: 1080
	image width: 1920

```
