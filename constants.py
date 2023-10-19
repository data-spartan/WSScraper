import pandas as pd
import base64
from os import getenv
from dotenv import load_dotenv

load_dotenv(".env")

scrapoxy_admin_pass_base64 = base64.b64encode(
getenv("adm_pass_scrapoxy").encode('ascii'))

sports={'Football': '1',
 
}

football_periods_translation = {
    "1": 1,
    "finished":0,
    "Half Time": 6,
    "2": 2,
    "timeout": 8,
    "paused":7,
    "3":3,
    "4":4,
    "penalties":5
}


sport_translations = {
    "Soccer": "Football",
    # "Basketball": "Basketball",
    # "Tennis": "Tennis",
    # "Ice Hockey": "Ice Hockey",
    # "Darts": "Darts",
    # "Snooker": "Snooker",
    # "Cricket": "Cricket",
    # "Boxing": "Boxing",
    # "MMA": "MMA",
    # "Volleyball": "Volleyball",
    # "Handball": "Handball",
    # "Rugby": "Rugby",
    # "American Football": "American Football",
    # "Badminton": "Badminton"
}
#allowed_string_times = ["HT" , "Ended", "Paused", "In progress", "End of 1st Quarter", "End of 2nd Quarter", "End of 3rd Quarter", "Penalties", "1. set", "2. set", "3. set", "4. set", "5. set"]

# random_ids_list=pd.read_csv(getenv("ids_random_path"),header=None)[0].to_list()

prod_conf = {'bootstrap.servers': "localhost:9092",
            'client.id': "live_feed",
            "message.max.bytes": 22285880,
            # "queue.buffering.max.messages":10,
            # "batch.num.messages":1,
            "linger.ms":10,
            "acks": 1,
            "debug":"msg",
            "compression.type":"gzip"}
