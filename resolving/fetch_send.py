import logging
import redis.client
from os import getenv
from constants import sport_translations
from time import time
# from utils.resolvers import resolve_football
from dataclasses import dataclass,field
from typing import Dict,List
# from scoreboard_generators import *
from redis_db import redis_service
from logger.log_func import logging_func
from resolving.resolvers import ResolverAdapter
from utils.scoreboard_generators import generate_football_scoreboard
from datetime import datetime
from resolving.allowed_resolving_games import allowed_games

@dataclass
class FetchSend:
    redis_result: redis_service = field(default=None)
    redis_market: redis_service = field(default=None)
    redis_mapped_markets_ids: redis_service = field(default=None)

    # resolved_queue: ResolvingQueue = field(default_factory=ResolvingQueue, repr=False)
    
    def __post_init__(self):
        self.resolver=ResolverAdapter(self.redis_result,self.redis_market)
        self.logg = logging_func("sending-data", getenv("SENDER_LOGS"))[1]  # get only logger object
        # self.sport_container={"sport":{"Football":[],"Basketball":[]},"source":"instant_bet"}
        self.fixtures_array={'fixtures':[]}
        self.resolved_array= {'resolved':[]}

    def generate_live_fixtures(self,data: List[Dict]) -> List[Dict]:
        mapped_markets_ids=self.redis_mapped_markets_ids.load_miss('missing_markets_ids') #already mapped markets ids
        for row in data:
            if row:
                try:
                    match_data = {
                        'source': 'instant-bet',
                        'type': 'live',
                        'fixtureId': row['ItemId'],
                        'competitionString': f"{sport_translations[row['sport']] if row['sport'] in sport_translations.keys() else row['sport']}|{row['country_name']}|{row['TournamentName']}",
                        'region': row['country_name'],
                        'regionId': row['country_id'],
                        'sport': sport_translations[row['sport']] if row['sport'] in sport_translations.keys() else row['sport'],
                        'sportId': row['sport_id'],
                        'competition': row['TournamentName'],
                        'competitionId': row['TournamentId'],
                        'fixtureTimestamp': row['event_start_time'],
                        'competitor1': row['home_name'],
                        'competitor1Id': row['home_id'],
                        'competitor2': row['away_name'],
                        'competitor2Id': row['away_id'],
                        'sentTime':'2023-11-13T11:59:38.274+00:00',#datetime.now().isoformat(),
                        'games':[]
                    }
                    row['games'][:]=(i for i in row['games'] if i['type'] in allowed_games) #send only allowd games bcs resolved games and available games must be in sync
                    match_data['games']=row['games']
                    if row['event_period'] == "timeout":
                        if int(time()) - int(row['event_fetched_timestamp']) > 40:
                            row['event_period'] = "Ended"
                    
    
                    if row['sport'] in ['Soccer', 'Football']:
                        arr_resolved, statistics = self.resolver.resolve_football(row)
                        # arr_resolved=[{
                        #         "id":None,
                        #         "type": 'Correct Score|6-0',
                        #         "status": "won"
                        #         },
                        #         {
                        #             "id":None,
                        #         "type": "Both Teams To Score|No",
                        #         "status": "lost"
                        #         }
                        #         ]
                                

                    if row['event_period'] != "Ended":
                        status="In progress"
                    else:
                        status="Ended"
                     
                    
                    if arr_resolved:
                        for i in arr_resolved:#mapp resolved games
                            if marketId:=(mapped_markets_ids.get(i['type'])):
                                i['id']=marketId
                        arr_resolved[:]=(i for i in arr_resolved if i['id']) #filterout resolved games with none id
                        self.resolved_array['resolved'].append({'fixtureId':row['ItemId'],'status':status,'resolved':arr_resolved})
                        
                    match_data['scoreboard'] = generate_football_scoreboard(statistics,row['event_seconds'],row['event_period'],row['event_fetched_timestamp'])         

                    self.fixtures_array['fixtures'].append(match_data)

                except Exception as e:
                    self.logg.error(f"In generate_live_fixtures. Error {e}; Fixture id: {row['ItemId']}")                
                    continue
        # self.fixtures_array['fixtures'][:]=(i for i in self.fixtures_array['fixtures'] if i['games'])
        return self.fixtures_array, self.resolved_array
    
    def fetch_and_send(self):
        res=self.redis_result.load_results_data()
        mark=self.redis_market.load_markets_data()
        for i in res:
            for j in mark:
                """
                checking if markets are empty list(if there are no previous markets so we save empty list in redis);if ItemId in markets bcs in previous iteration we
                deleted ItemId so it would throw and error otherwise; regarding perf, only checking if first element of markets equals result ItemId;
                """
                if (j and "ItemId" in j[0]) and (j[0]["ItemId"] == i["ItemId"]):
                    i["games"]=j
                    for k in i["games"]:
                        del k["ItemId"]
                    break
                else:
                    i["games"]=[]
        res[:] = (i for i in res if i['home_id'] and i['away_id'] and i["games"])
        #check if there is homeid,awayid, games that is empty and filter them out
        self.generate_live_fixtures(res)
        return
  
  