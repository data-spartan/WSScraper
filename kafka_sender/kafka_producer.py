import json
import time
from dataclasses import dataclass,field
import orjson
from confluent_kafka import Producer,Message


class Producer_:

    def __init__(self,conf,topic,partition=None):
        self.producer_instance: Producer = Producer(conf)
        self.topic = topic
        # self.partition = partition  ##left in case key hasing is not good option

    def serializer_(self,payload:dict) -> bytes:
        # print(payload)
        return orjson.dumps(payload)

    def acked(self,err, msg:Message):
        if err is not None:
            print(f"Failed to deliver message: {str(msg)}: {str(err)}")
        else:
            print(f"Message produced: {str(msg.value)}")

    def sender(self,data):
        try:
            # for sport in data["sport"]:
            if data['fixtures']:
                self.producer_instance.produce(topic=self.topic, value=self.serializer_(data),callback=self.acked)
            self.producer_instance.poll(0)

        except BufferError as error:
            self.producer_instance.poll(1)

            self.producer_instance.produce(self.topic, value=self.serializer_(data),callback=self.acked)
            

            self.producer_instance.flush()

if __name__ == '__main__':
    "batch.num.messages"
    prod_conf = {'bootstrap.servers': "localhost:9092,localhost:9093",
            'client.id': "instant_bet",
            "message.max.bytes": 22285880,
            "queue.buffering.max.messages":10,
            "batch.num.messages":1,
            "linger.ms":10,
            "acks": 1,
            "debug":"msg",
            "compression.type":"gzip"}


    # data = [{"instant_bet": {"markets": [{"ng1": 2}], "resolved": [{"ng1": "won"}]}},
    #         {"instant_bet": {"markets": [{"finre1": 2}], "resolved": [{"finres1": "lost"}]}}]
    with open('/home/neotech/PycharmProjects/instant_bet_dynamic/data/markets_dynamic.json', 'r') as outfile:
        data=json.loads(outfile.read())
        #data=data["sport"][

    producer_ = Producer_(prod_conf,topic="test1-topic",partition=0)

    while True:
        #try:
        producer_.sender(data)
        time.sleep(10)