#!/bin/bash
cd ~/Downloads/kafka_2.11-1.0.0/
bin/zookeeper-server-start.sh config/zookeeper.properties &
#bin/kafka-server-start.sh config/server.properties &
bin/kafka-server-start.sh config/server-1.properties &
bin/kafka-server-start.sh config/server-2.properties &
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic my-replicated-topic &
bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic
cd ~/bin

~/Downloads/kafka_2.11-1.0.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9093 --topic my-replicated-topic | ./reg_event_kafka_consumer.py &
./client.py # using  ~/Downloads/kafka_2.11-1.0.0/bin/kafka-console-producer.sh --broker-list localhost:9094 --topic my-replicated-topic

