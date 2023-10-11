import pandas as pd
import base64
from os import getenv
from dotenv import load_dotenv

load_dotenv(".env")

scrapoxy_admin_pass_base64 = base64.b64encode(
getenv("adm_pass_scrapoxy").encode('ascii'))

sports={'Football': '1',
 # 'Ice Hockey': '2',
 # 'Basketball': '3',
 # 'Tennis': '4',
 # 'Volleyball': '5',
 # 'American Football': '6',
 # 'Badminton': '9',
 # 'Baseball': '11',
 # 'Beach Football': '12',
 # 'Beach Volleyball': '14',
 # 'Cricket': '19',
 # 'Darts': '22',
 # 'Formula 1': '25',
 # 'Futsal': '26',
 # 'Handball': '29',
 # 'Rugby Union': '37',
 # 'Table Tennis': '41',
 # 'MMA': '44',
 # 'Counter-Strike: GO': '75',
 # 'Dota 2': '76',
 # 'King of Glory': '158',
 # 'Basketball Shots': '205',
 # 'League of Legends: Wild Rift': '240'
}

football_periods_translation = {
    "1": 101,
    "Ended": 111,
    "HT": 102,
    "2": 103,
    "Paused": 100,
    "3":1,
    "4":2
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

