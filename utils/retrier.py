import functools
from time import sleep
import logging
from functools import wraps

auto_rec = logging.getLogger("websocket.auto_recovery")

def auto_recovery(func):
    def wrapper(*args,**kwargs):
        for i in range(10):
            try:
                return func(*args,**kwargs)
            except Exception as err:
                auto_rec.info('Trying to reconnect;')
                error = err
                sleep(3)
                continue
        else:
            auto_rec.error(f'Terminating web socket after {i+1} attempts due to error: \n{error};')
            raise error
    return wrapper

