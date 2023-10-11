import uvloop
from time import time,sleep
#from utils.kafka_producer import send_notification
from utils.redisHash import *
from utils.fetch_send import *
from utils.async_sender import *



if __name__ == "__main__":
    uvloop.install()
    send=AsyncSender()

    results_hash = RedisHash(db_id=7, key_field='ItemID')
    markets_hash = RedisHash(db_id=8, key_field='ItemID')

    logg=logging_func("sender",getenv("sender_logs"))[1] #get only logger object

    fetch_send=FetchSend(redis_result=results_hash,redis_market=markets_hash)
    logg.info(f"STARTING neotech_3 live SENDER")
    # send_notification(
    #     {
    #         'source': 'neotech_3 live sender',
    #         'severity': 'NOTIFICATION',
    #         'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
    #         'message': 'starting'
    #     }
    # )
    while True:
        try:
            markets,resolved_live = fetch_send.fetch_and_send()
            asyncio.run(send.send_all_markets(markets))

            """
            adding condition for resolve_live bcs most of the time this variable is empty. 
            asyncio.run(send_all_resolved_live(resolved_live)) is called only if resolved_live has resolved games,
            so we get performance boost of cca 6 %.
            """
            asyncio.run(send.send_all_resolved_live(resolved_live)) if resolved_live else None
            sleep(3)
        except KeyboardInterrupt:
            logg.warning(f"neotech_3 live sender closed manually")
            # error_message = {
            #     'source': 'neotech_3 live sender',
            #     'severity': 'WARNING',
            #     'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            #     'message': "scraper closed manually"
            # }
            # send_notification(error_message)
            raise

        except Exception as e:

            logg.error(f"neotech_3 live sender ERROR: {e}")
            # error_message = {
            #     'source': 'neotech_3 live sender',
            #     'severity': 'ERROR',
            #     'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            #     'message': str(e)
            # }
            # send_notification(error_message)
            raise

