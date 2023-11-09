from redis_db.redis_service import *
import uuid
from datetime import datetime


result_redis = RedisHash(db_id=7, key_field="ItemId",expiry_time=66000)
missing_keys = RedisHash(db_id=10, key_field="ItemId",expiry_time=66000)

# a={'stefan':1,'bogdan':2,'maka':3}
# b={'stefan'}
# existing=missing_keys.load_miss('b',list(a.keys()))



# print(set(a) - set(b))
# print(set(a).__len__())
# a={}
# a.update({'b':1, 'c':2})
# # print(a)
# print(existing)
fixt = [{"team":'United'},{"team":'Partizan'}]

result = filter(lambda x: x['team']=='United', fixt)
print((result)[0])


