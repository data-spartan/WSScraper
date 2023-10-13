import logging
import redis.client
from os import getenv
from constants import sport_translations
from time import time
# from utils.resolvers import resolve_football
from dataclasses import dataclass,field
from typing import Dict,List
from utils.queue import Queue, ResolvingQueue
# from scoreboard_generators import *
from utils import redis_hash
from utils.log_func import logging_func
from utils.resolvers import ResolverAdapter
from utils.scoreboard_generators import generate_football_scoreboard

@dataclass
class FetchSend:
    redis_result: redis_hash = field(default=None)
    redis_market: redis_hash = field(default=None)

    # resolved_queue: ResolvingQueue = field(default_factory=ResolvingQueue, repr=False)
    
    def __post_init__(self):
        self.resolver=ResolverAdapter(self.redis_result,self.redis_market)
        self.logg = logging_func("sending-data", getenv("sender_logs"))[1]  # get only logger object
        # self.sport_container={"sport":{"Football":[],"Basketball":[]},"source":"instant_bet"}
        self.fixtures_array={'fixtures':[]}

    def generate_live_fixtures(self,data: List[Dict],results_hash,markets_hash) -> List[Dict]:
        """
        form data for COU sending
        """
        # markets_queue=list()
        # _append=markets_queue.append
        for row in data:
            if row:
                try:
                    match_data = {
                        'source': 'instant-bet',
                        'type': 'live',
                        'fixtureId': row['ItemID'],
                        'competitionString': f"{sport_translations[row['sport']] if row['sport'] in sport_translations.keys() else row['sport']}|{row['country_name']}|{row['TournamentName']}",
                        'region': row['country_name'],
                        'sourceRegionId': row['country_id'],
                        'sport': sport_translations[row['sport']] if row['sport'] in sport_translations.keys() else row['sport'],
                        'sourceSportId': row['sport_id'],
                        'competition': row['TournamentName'],
                        'sourceCompetitionId': row['TournamentId'],
                        'fixtureTimestamp': row['event_start_time'],
                        'competitor1': row['home_name'],
                        'sourceCompetitor1Id': row['home_id'],
                        'competitor2': row['away_name'],
                        'sourceCompetitor2Id': row['away_id'],
                        'time': time(),
                        'statistics':row['stats'],
                        'games': row['games'] if row["games"] else []
                    }
                    if row['event_seconds'] == "Ended":
                        row['event_period'] = "Ended"
                    elif row['event_seconds'] == "Paused":
                        if int(time()) - int(row['event_fetched_timestamp']) > 40:
                            row['event_period'] = "Ended"

                    if row['sport'] in ['Soccer', 'Football']:
                        match_data["resolved"], statistics = self.resolver.resolve_football(row)
                        match_data['scoreboard'] = generate_football_scoreboard(statistics,row['event_seconds'],row['event_period'],row['event_fetched_timestamp'])
                        


                    if row['event_period'] == "finished":
                        results_hash.delete_key(row['ItemID'])
                        markets_hash.delete_key(row['ItemID'])

                    self.fixtures_array['fixtures'].append(match_data)

                except Exception as e:
                    self.logg.error(f"In generate_live_fixtures. Error {e}; Fixture id: {row['ItemID']}")                
                    continue
        return self.fixtures_array
    
    def fetch_and_send(self):
        res=self.redis_result.load_results_data()
        mark=self.redis_market.load_markets_data()
        for i in res:
            for j in mark:
                """
                checking if markets are empty list(if there are no previous markets so we save empty list in redis);if ItemID in markets bcs in previous iteration we
                deleted ItemID so it would throw and error otherwise; regarding perf, only checking if first element of markets equals result ItemID;
                """
                if (j and "ItemID" in j[0]) and (j[0]["ItemID"] == i["ItemID"]):
                    i["games"]=j
                    for k in i["games"]:
                        del k["ItemID"]
                    break
                else:
                    i["games"]=[]

        self.generate_live_fixtures(res,self.redis_result,self.redis_market)
  
  