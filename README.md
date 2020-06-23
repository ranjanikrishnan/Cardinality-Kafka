# Data Engineering - Kafka

- A detailed project description can be found [here](https://github.com/tamediadigital/hiring-challenges/tree/master/data-engineer-challenge)

### Prerequisites

- Docker
- Docker-compose
- Please find all the project dependencies in Pipfile

### Project Setup

1. Install Kafka
    ```
    docker-compose up -d
    ```
    - This will start zookeeper and kafka

2. Create a topic
    ```
    sudo docker exec -it kafka /bin/sh
    ```
    ```
    /opt/kafka/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic test
    ```

3. Sending test data to kafka topic using kafka producer
    - Run the following command from inside the docker container
        ```
        wget http://tx.tamedia.ch.s3.amazonaws.com/challenge/data/stream.jsonl.gz
        ```
        ```
        gunzip stream.jsonl.gz
        ```
        ```
        cat stream.jsonl | opt/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic sample
        ```
    - Alternatively run the following script
        ```
        python src/kafka/producer.py
        ```

4. A small app that reads this data from kafka and prints it to stdout 

    ```
    python src/kafka.consumer.py
    ```

5. Count distinct elements in a stream



### Project Details

- To be added