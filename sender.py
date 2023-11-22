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
    load_dotenv(find_dotenv(".env"))
    logg = logging_func("sender", getenv("SENDER_LOGS"))[1]
    logg.info("SENDER started...")

    results_hash = RedisHash(port=getenv("REDIS_PORT"),db_id=getenv("RESULTS_REDIS"), key_field='ItemId')
    markets_hash = RedisHash(port=getenv("REDIS_PORT"),db_id=getenv("MARKETS_REDIS"), key_field='ItemId')
    missing_ids_hash = RedisHash(port=getenv("REDIS_PORT"),db_id=getenv("MISSING_IDS_REDIS"),expiry_time=66000)

    fetchsend = FetchSend(results_hash,markets_hash,missing_ids_hash)
    
    prod_conf["bootstrap.servers"]=getenv("HOST_ADDRESS_KAFKA")
    producer_instance=Producer_(prod_conf,getenv('KAFKA_FIXT_TOPIC'),getenv('KAFKA_RESOLV_TOPIC'))

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
            producer_instance.sender(fetchsend.fixtures_array,fetchsend.resolved_array)
            # [(results_hash.delete_key(i['fixtureId']),markets_hash.delete_key(i['fixtureId'])) for i in fetchsend.resolved_array["resolved"] if i['status'] == "Ended"]
            fetchsend.fixtures_array['fixtures'].clear()
            fetchsend.resolved_array['resolved'].clear()
            sleep(3)
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

