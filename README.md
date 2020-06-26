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
    docker exec -it kafka /bin/sh
    ```
    ```
    /opt/kafka/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic kafka_distinct_counter
    ```

- Export environment variables within the .env file

    ```
    export $(cat .env | grep -v ^# | xargs)
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
        cat stream.jsonl | opt/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic kafka_distinct_counter
        ```
    - Alternatively run the following (outside the container, within the project folder)
        ```
        wget http://tx.tamedia.ch.s3.amazonaws.com/challenge/data/stream.jsonl.gz
        ```
        ```
        gunzip stream.jsonl.gz
        ```
        ```
        python src/kafka/producer.py
        ```

4. A small app that reads this data from kafka and prints it to stdout 

    ```
    python src/kafka/consumer.py
    ```

5. Count distinct elements in a stream

- For counting distinct items in a kafka stream, 
    [Faust](https://faust.readthedocs.io/en/latest/) has been used, which is a stream processing library
- Run the following:
    - In a terminal window, start the faust worker
        ```
        cd src/distinct_counter
        ```
        ```
        faust -A users worker -l info
        ```
    - In another terminal window, publish the data using the producer
        ```
        python src/kafka/producer.py
        ```
    - In another terminal window, run the consumer and listen to the topic to which the faust worker writes the output 
        ```
        opt/kafka/bin/kafka-console-consumer.sh --from-beginning --bootstrap-server kafka:9092 --topic=users-unique-changelog
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
- Refer [here](http://highscalability.com/blog/2012/4/5/big-data-counting-how-to-count-a-billion-distinct-objects-us.html)


### Project Improvements

- Dynamically configure the interval for the count of unique users (per-minute/per-hour/per-day)
- Store each configurable interval counts with timestamp in a separate topic
- For scalability, define kafka nodes which would read from one or more topics and generate unique users count accordingly

### References
- http://highscalability.com/blog/2012/4/5/big-data-counting-how-to-count-a-billion-distinct-objects-us.html

- https://faust.readthedocs.io/en/latest/