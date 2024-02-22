sudo docker run -it --name consumer_1 --gpus all --network kafka_network -v `pwd`:/ITMS/ safeproaivideo/itms:kafka-base-gpu 
