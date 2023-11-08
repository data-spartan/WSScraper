from dataclasses import dataclass
import orjson
import redis

"""
creating references for each function that are called in a loop, in order to boost perf for cca 7 % 
"""
_key=dict.keys
_list=list
_dumps=orjson.dumps
_loads=orjson.loads

@dataclass
class RedisHash:
    db_id: int
    key_field: str = None
    list_name: str = None
    hash_name:str=None
    expiry_time: int = 100
    """
    Setting None as default value makes init attributes optional
    """
    def __post_init__(self):
        self.connection_pool_=redis.ConnectionPool(max_connections=30,db=self.db_id, decode_responses=True)
        self.__redis: redis.client.Redis = redis.Redis(password=None,db=self.db_id,connection_pool=self.connection_pool_)
        # self.__redis: redis.client.Redis = redis.Redis(db=self.db_id)

    def flush(self):
        self.__redis.flushdb()

    def delete_key(self, key: int):
        self.__redis.delete(key)

    def save_results(self, formatted: list):
        """
        when ws conn is first time established with betconstruct provider, we receive bulk detailed resposne data with all
        current matches. We then bulk write into the redis from which we use inserted data for data change comparsion data.
        """
        with self.__redis.pipeline() as pipe:
            for i in formatted:
                pipe.set(i[self.key_field], _dumps(i))
                pipe.expire(i[self.key_field], self.expiry_time)
            pipe.execute()

    def save_markets(self, formatted: list):
        """
        when ws conn is first time established with betconstruct provider, we receive bulk detailed resposne data with all
        current markets. We then bulk write into the redis from which we use inserted data for data change comparsion data.
        """
        with self.__redis.pipeline() as pipe:
            for i in formatted:
                pipe.set(_list(_key(i))[0], _dumps(i[_list(_key(i))[0]]))
                pipe.expire(_list(_key(i))[0], self.expiry_time)
            pipe.execute()

    def write_results_history(self, result_key: int, gems: str):
        """
        caching last changed games result in current set. can be used for any game
        in any sport if neccessary for resolving
        """
        self.__redis.rpush(result_key, gems)


    def load_results_history(self, key: int):
        """
        loads 3 last games result in current set, example Tennis: 1:0,1:1,2:1
        can be used for any game, any sport if neccessary for resolving live or prematch games.
        In this case we loaded only 3 latest games,
        because we need it only for tennis live resolving right now
        """
        history=self.__redis.lrange(key,-3,-1)
        return history if history else False

    def load_results_data(self) -> list:
        """
        loads data from the redis
        """
        with self.__redis.pipeline() as pipe:
            for key in self.__redis.keys():
                pipe.get(key)
            result=pipe.execute()
        result=_list(map(_loads,result)) if result else _list()
        return result

    def load_markets_data(self) -> list:
        """
        loads data from the redis;if there are empty markets for first time saving to redis, returns empty list
        """
        with self.__redis.pipeline() as pipe:
            for key in self.__redis.keys():
                pipe.get(key)
            result=pipe.execute()
        result=_list(map(_loads,result))
        return result if result else _list()

    def save_missing_keys(self,data):
        with self.__redis.pipeline() as pipe:
            for i in data:
                pipe.rpush(self.list_name,_dumps(i))
            pipe.execute()

    def load_missing_keys(self):
        res=self.__redis.lrange(self.list_name,0,-1)
        return _list(map(_loads,res)) if res else _list()

    def write_missing_ids(self,hash:str,object):
        if object:
            self.__redis.hmset(hash,object)

    def load_miss(self,hash:str,fields:list=None):
        return self.__redis.hgetall(hash)