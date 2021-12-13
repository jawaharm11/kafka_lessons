from confluent_kafka import Consumer
from time import sleep

class KafkaConsumer:
    broker = "localhost:39092"
    topic = "lesson1"
    group_id = "consumer-1"

    def start_listener(self):
        consumer_config = {
            'bootstrap.servers': self.broker,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': 'true',
            'max.poll.interval.ms': '86400000',
        }

        consumer = Consumer(consumer_config)
        consumer.subscribe([self.topic])

        try:
            while True:
                print(f"Consuming from topic {self.topic}")
                # read single message at a time
                msg = consumer.poll(0)

                if msg is None:
                    sleep(5)
                    continue
                if msg.error():
                    print("Error reading message : {}".format(msg.error()))
                    continue
                # You can parse message and save to data base here
                print(f'Message from partition {msg.partition()} at offset {msg.offset()}, {msg.value()}')
                consumer.commit()

        except Exception as ex:
            print("Kafka Exception : {}", ex)

        finally:
            print("closing consumer")
            consumer.close()

#RUNNING CONSUMER FOR READING MESSAGE FROM THE KAFKA TOPIC
kafka_consumer = KafkaConsumer()
kafka_consumer.start_listener()