from os import getenv
from dotenv import load_dotenv,find_dotenv
import json
import time
from dataclasses import dataclass,field
import orjson
from confluent_kafka import Producer,Message
from logger.log_func import *


class Producer_:

    def __init__(self,conf,fixt_topic,resolv_topic,partition=None):
        self.producer_instance: Producer = Producer(conf)
        self.fixtures_topic = fixt_topic
        self.resolved_topic = resolv_topic
        self.chunk_size=10
        self.__post_init__()
        # self.partition = partition  ##left in case key hasing is not good option


    def __post_init__(self):
        load_dotenv(find_dotenv(".env"))
        self.logg = logging_func("producer", getenv("SENDER_LOGS"))[1]


    def serializer_(self,payload:dict) -> bytes:
        # print(payload)
        return orjson.dumps(payload)

    def retry_produce(self, msg: Message, retry_count:int):
        retries = 0
        while retries < retry_count:
            try:
                self.logg.warning(f"Retrying to produce message, attempt {retries + 1}/{retry_count}")
                self.producer_instance.produce(topic=msg.topic(), value=msg.value(), callback=self.acked)
                self.producer_instance.poll(0)
                break  # Break the loop if the produce is successful
            except BufferError as e:
                self.producer_instance.poll(1)
                time.sleep(1)  # Add a delay before retrying
                retries += 1

        if retries == retry_count:
            self.logg.error(f"Failed to produce message after {retry_count} attempts: {str(msg.topic())}")

    def acked(self,err, msg:Message, retry_count=10):
        if err is not None:
            self.logg.error(f"Failed to deliver message: {str(msg)}: {str(err)}")
            self.retry_produce(msg, retry_count)
        else:
            self.logg.info(f"Message produced: {str(msg.topic())}")

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

        except BufferError as bufferror:
            self.producer_instance.poll(1)
            self.producer_instance.produce(self.topic, value=self.serializer_(fixtures),callback=self.acked)
            self.producer_instance.flush()
            self.logg.warning(f"Flushed messages due to: {bufferror}")
        except Exception as err:
            raise err

