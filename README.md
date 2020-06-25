# Data Engineering - Kafka

- A detailed project description can be found [here](https://github.com/tamediadigital/hiring-challenges/tree/master/data-engineer-challenge)

### Prerequisites

- Docker
- Docker-compose
- Please find all the project dependencies in requirements.txt

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

- For counting distinct items in a kafka stream, 
    [Faust](https://faust.readthedocs.io/en/latest/) has been used, which is a stream processing library
    Run the following:
    - In a terminal window, start the faust worker
        ```
        cd src/distinct_counter
        ```
        ```
        faust -A sample worker -l info
        ```
    - Publish the data using the producer
        ```
        python src/kafka/producer.py
        ```
    - Run the consumer and listen to the topic to which the faust worker writes the output 
        ```
        ./kafka-console-consumer.sh --from-beginning --bootstrap-server kafka:9092 --topic=sample-sample-changelog
        ```

6. Benchmark
   - To be added

7. Output to a new Kafka Topic instead of stdout
    - Already done in step 5
    - Faust writes the output to a new topic
    - By default the changelog topic for a given Table has the format <app_id>-<table_name>-changelog

 - Alternatively some efficient cardinality algorithms can be used:
    - Hashset
    - Hyperloglog
- Refer [here](big-data-counting-how-to-count-a-billion-distinct-objects)


### Project Details

- To be added