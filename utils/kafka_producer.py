"""
this is kafka producer function

idea behind this is to send
"""
import json
from os import getenv

from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv(".env")
kafka_host=getenv('HOST_ADDRESS_KAFKA')

# Messages will be serialized as JSON
def serializer(message) -> bytes:
    return json.dumps(message).encode('utf-8')




def send_notification(message: dict) -> None:
    """
    sends

    :param message:
    :return:
    """
    # producer = KafkaProducer(
    #     bootstrap_servers=kafka_host,
    #     value_serializer=serializer,
    #     acks='all')
    # producer.send('scraper_notifications',
    #               message)
    # producer.flush()
    # producer.close()
    # return

if __name__ == '__main__':
    pass
