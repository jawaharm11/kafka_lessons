from confluent_kafka import avro 
from confluent_kafka.avro import AvroProducer

import json
import uuid


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


def send_record():
    
    key_schema, value_schema = load_avro_schema_from_file(schema_file)

    producer_config = {
        "bootstrap.servers": boostrap_servers,
        "schema.registry.url": 'http://localhost:8081'
    }

    record_value = '{"email": "test@email.com", "firstName": "Jane", "lastName": "Doe"}'

    producer = AvroProducer(producer_config, default_key_schema=key_schema, default_value_schema=value_schema)

    key =  str(uuid.uuid4())
    value = json.loads(record_value)

    try:
        producer.produce(topic=topic, key=key, value=value)
    except Exception as e:
        print(f"Exception while producing record value - {value} to topic - {topic}: {e}")
    else:
        print(f"Successfully produced record value - {value} to topic - {topic}")

    producer.flush()


if __name__ == "__main__":
    send_record()