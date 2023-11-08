from redis_db.redis_service import *
import uuid
from datetime import datetime


result_redis = RedisHash(db_id=7, key_field="ItemID",expiry_time=66000)
missing_keys = RedisHash(db_id=10, key_field="ItemID",expiry_time=66000)

# a={'stefan':1,'bogdan':2,'maka':3}
# b={'stefan'}
# existing=missing_keys.load_miss('b',list(a.keys()))
existing=missing_keys.load_miss('miss_teams')


# print(set(a) - set(b))
# print(set(a).__len__())
# a={}
# a.update({'b':1, 'c':2})
# # print(a)
# print(existing)
fixt = {"team1":'United', "team2":"City"}
new = {}
# for i in existing:
if not existing.get(fixt['team1']):
    new.update({fixt['team1']:uuid.uuid1().__str__()})
if not existing.get(fixt['team2']):
    new.update({fixt['team2']:uuid.uuid1().__str__()})

existing.update(new)
missing_keys.write_miss('miss_teams',new)
print(existing,new)

# if existing.__len__()>fixt.__len__():
#     missing_keys.write_miss('b',keyVal)

def fill_missing_data_keys(self, data,existing_teams):
    new = {}
    for fixt in data:        
        
        if not existing.get(fixt['team1']):
            new.update({fixt['team1']:uuid.uuid1().__str__()})
        if not existing.get(fixt['team2']):
            new.update({fixt['team2']:uuid.uuid1().__str__()})

        existing.update(new)
        return data, new
        




