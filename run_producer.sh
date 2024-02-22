sudo docker run -it --gpus all -v `pwd`:/ITMS/ --name producer --network kafka_network safeproaivideo/itms:kafka-base-gpu
