from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka import avro 


topic = "lesson1"
boostrap_servers = "localhost:29092"
schema_file = "schema.avsc"

def load_avro_schema_from_file(schema_file):
    key_schema_string = """
    {"type": "string"}
    """

    key_schema = avro.loads(key_schema_string)
    value_schema = avro.load(schema_file)

    return key_schema, value_schema


def consume():

    consumer_config = {
        "bootstrap.servers": boostrap_servers,
        "schema.registry.url": 'http://localhost:8081',
        "group.id": "test"
    }

    c = AvroConsumer(consumer_config)

    c.subscribe([topic])

    while True:
        try:
            msg = c.poll(10)

        except SerializerError as e:
            print("Message deserialization failed for {}: {}".format(msg, e))
            break

        if msg is None:
            continue

        if msg.error():
            print("AvroConsumer error: {}".format(msg.error()))
            continue

        print(f"Key: {msg.key()}, Value: {msg.value()}")

    c.close()

if __name__ == "__main__":
    consume()