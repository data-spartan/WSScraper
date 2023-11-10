from redis_db.redis_service import *
import uuid
from datetime import datetime


result_redis = RedisHash(db_id=7, key_field="ItemId",expiry_time=66000)
missing_keys = RedisHash(db_id=10, key_field="ItemId",expiry_time=66000)

# market={23433050: [{'OddsTypeName': 'Total Goals Odd/Even', 'quote': 1.58, 'sourceGameId': '1370271904Even', 'ItemId': 23433050, 'locked': False, 'type': 'Total Goals Odd/Even|Even'}, {'OddsTypeName': 'Total Goals Odd/Even', 'quote': 2.45, 'sourceGameId': '1370271904Odd', 'ItemId': 23433050, 'locked': False, 'type': 'Total Goals Odd/Even|Odd'}]}
if m:=(1<2):
    print(m)
