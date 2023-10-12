from os import getenv
from dotenv import load_dotenv,find_dotenv
import uvloop
from time import time,strftime,localtime
from time import sleep
import asyncio
from utils.kafka_producer import send_notification
from utils.redis_hash import RedisHash
from utils.fetch_send import FetchSend
from utils.async_sender import AsyncSender
from constants import prod_conf
from utils.log_func import *
from kafka_sender.kafka_producer import Producer_



if __name__ == "__main__":
    uvloop.install()
    load_dotenv(find_dotenv(".env.production"))
    logg = logging_func("sender", getenv("sender_logs"))[1]
    logg.info("SENDER started...")

    results_hash = RedisHash(db_id=getenv("results_redis"), key_field='ItemID')
    markets_hash = RedisHash(db_id=getenv("markets_redis"), key_field='ItemID')
    results_history_list=RedisHash(db_id=getenv("history_redis"), key_field='ItemID')

    fetchsend = FetchSend(results_hash,markets_hash,results_history_list)
    producer_instance=Producer_(prod_conf,"test1-topic")

    send_notification(
        {
            'source': 'neofeed_live_1 sender',
            'severity': 'NOTIFICATION',
            'timestamp': strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'message': 'starting'
        }
    )
    while True:
        try:
            fetchsend.fetch_and_send()
            producer_instance.sender(fetchsend.match_array)
            fetchsend.match_array.clear()
            
            sleep(10)
        except KeyboardInterrupt:
            error_message = {
                'source': 'neofeed_live_1 sender',
                'severity': 'WARNING',
                'timestamp': strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
                'message': "scraper closed manually"
            }
            send_notification(error_message)
            raise

        except Exception as e:
            error_message = {
                'source': 'neofeed_live_1 sender',
                'severity': 'ERROR',
                'timestamp': strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
                'message': str(e)
            }
            logg.error(f"SENDER ERROR: {e}", exc_info=True)
            send_notification(error_message)
            raise

