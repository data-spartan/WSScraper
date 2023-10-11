from utils.redisHash import *
from utils.ws_interface import *
from constants import *
global random_ids_list


if __name__ == "__main__":
    load_dotenv(".env")

    result_redis = RedisHash(db_id=7, key_field="ItemID")
    markets_redis = RedisHash(db_id=8, key_field="ItemID",expiry_time=1000)
    miss_keys_redis = RedisHash(db_id=9,list_name="missing_teams_id")
    ws=WebsocketClient(ws_url=getenv("ws_url"),miss_keys_redis=miss_keys_redis,markets_redis=markets_redis,result_redis=result_redis)
    ws.connection()

