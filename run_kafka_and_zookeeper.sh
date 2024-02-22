docker run -d --name zookeeper --network kafka_network wurstmeister/zookeeper
#docker run -d --name kafka --network kafka_network -p 9092:9092 \
#	-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 \
#	-e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT \
#	-e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
#	-e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 wurstmeister/kafka
docker run -d --name kafka --network kafka_network -p 9092:9092 \
    -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 \
    -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 \
    -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT \
    -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
    -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 wurstmeister/kafka

