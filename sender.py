from os import getenv
from dotenv import load_dotenv,find_dotenv
from time import time,strftime,localtime
from time import sleep
from utils.kafka_notifier import send_notification
from redis_db.redis_service import RedisHash
from resolving.fetch_send import FetchSend
from constants import prod_conf
from logger.log_func import *
from kafka_sender.kafka_producer import Producer_



if __name__ == "__main__":
    load_dotenv(find_dotenv(".env.production"))
    logg = logging_func("sender", getenv("sender_logs"))[1]
    logg.info("SENDER started...")

    results_hash = RedisHash(db_id=getenv("results_redis"), key_field='ItemID')
    markets_hash = RedisHash(db_id=getenv("markets_redis"), key_field='ItemID')

    fetchsend = FetchSend(results_hash,markets_hash)
    producer_instance=Producer_(prod_conf,getenv('kafka_topic'))

    send_notification(
        {
            'source': 'instant_bet sender',
            'severity': 'NOTIFICATION',
            'timestamp': strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
            'message': 'starting'
        }
    )
    while True:
        try:
            fetchsend.fetch_and_send()
            producer_instance.sender(fetchsend.fixtures_array)
            [fetchsend.fixtures_array[i].clear() for i in fetchsend.fixtures_array]
            sleep(10)
        except KeyboardInterrupt:
            error_message = {
                'source': 'instant_bet sender',
                'severity': 'WARNING',
                'timestamp': strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
                'message': "scraper closed manually"
            }
            send_notification(error_message)
            raise

        except Exception as e:
            error_message = {
                'source': 'instant_bet sender',
                'severity': 'ERROR',
                'timestamp': strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
                'message': str(e)
            }
            logg.error(f"SENDER ERROR: {e}", exc_info=True)
            send_notification(error_message)
            raise

