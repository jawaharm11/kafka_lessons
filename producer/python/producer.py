from confluent_kafka import Producer

class KafkaProducer:
    broker = "localhost:29092"
    topic = "lesson1"
    producer = None

    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': self.broker,
            'retries': 3,
            'socket.timeout.ms': 10000,
            'linger.ms': 10,
            'batch.size': 20000,
            'api.version.request': 'false',
            'broker.version.fallback': '0.9.0',
        })

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to topic {} partiton:[{}] offset:[{}]'.format(
                msg.topic(), msg.partition(), msg.offset()))

    def send_msg_async(self, msg):
        print("Send message asynchronously")
        self.producer.produce(
            self.topic,
            msg,
            callback=lambda err, original_msg=msg: self.delivery_report(err, original_msg),
        )
        self.producer.flush()

    def send_msg_sync(self, msg):
        print("Send message synchronously")
        for i in range(101,200):
            msg = f"msg-{str(i)}"
            self.producer.produce(
                self.topic,
                msg,
                callback=lambda err, original_msg=msg: self.delivery_report(
                    err, original_msg
                ),
            )
        self.producer.flush()


#SENDING DATA TO KAFKA TOPIC
kafka_producer = KafkaProducer()
message = "Test Message"
kafka_producer.send_msg_sync(message)