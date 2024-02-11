from kafka import KafkaProducer
import json
from django.conf import settings

def send_kafka_message(topic, message):
    producer = KafkaProducer(bootstrap_servers=[f'{settings.KAFKA_SERVER_IP}:9092'],
                             value_serializer=lambda m: json.dumps(m).encode('ascii'))
    producer.send(topic, message)
    producer.close()
