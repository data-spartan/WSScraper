import json
import time
from dataclasses import dataclass,field
import orjson
from confluent_kafka import Producer,Message


class Producer_:

    def __init__(self,conf,fixt_topic,resolv_topic,partition=None):
        self.producer_instance: Producer = Producer(conf)
        self.fixtures_topic = fixt_topic
        self.resolved_topic = resolv_topic
        self.chunk_size=10
        # self.partition = partition  ##left in case key hasing is not good option

    def serializer_(self,payload:dict) -> bytes:
        # print(payload)
        return orjson.dumps(payload)

    def acked(self,err, msg:Message):
        if err is not None:
            print(f"Failed to deliver message: {str(msg)}: {str(err)}")
        else:
            print(f"Message produced: {str(msg.value)}")

    def partition(self,data: list, chunk_size: int) -> list:
        """
        partition data in chunks in order to distribute those chunks to different cpu cores
        """
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]
    
    def calculate_chunk_size(self,fixtures:list):
        if len(fixtures)%self.chunk_size==0:
            group_size=len(fixtures)//self.chunk_size
        else:
            leftover=len(fixtures)//self.chunk_size
            group_size=leftover+(len(fixtures)%self.chunk_size)

        return [chunk for chunk in self.partition(fixtures,group_size)]

    def sender(self,fixtures,resolved):
        try:
            if fixtures:=(fixtures['fixtures']):
                chunks=self.calculate_chunk_size(fixtures)
                for i in chunks:
                    self.producer_instance.produce(topic=self.fixtures_topic,value=self.serializer_(i),callback=self.acked)
                self.producer_instance.poll(0)

            if resolved:=(resolved['resolved']):
                chunks=self.calculate_chunk_size(resolved)
                for i in chunks:
                    self.producer_instance.produce(topic=self.resolved_topic, value=self.serializer_(i),callback=self.acked)
                self.producer_instance.poll(0)

        except BufferError as error:
            self.producer_instance.poll(1)
            self.producer_instance.produce(self.topic, value=self.serializer_(fixtures),callback=self.acked)
            self.producer_instance.flush()
