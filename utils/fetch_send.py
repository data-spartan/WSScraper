import logging
import redis.client
from constants import sport_translations
from time import time
from utils.resolvers import resolve_football
from dataclasses import dataclass,field
from typing import Dict,List
# from scoreboard_generators import *
from utils import redisHash

@dataclass
class FetchSend:
    redis_result: redisHash = field(default=None)
    redis_market: redisHash = field(default=None)

    def generate_live_fixtures(self,data: List[Dict]) -> List[Dict]:
        """
        form data for COU sending
        """
        markets_queue=list()
        _append=markets_queue.append
        for row in data:
            match_data = {
                'source': 'neofeed_live_3',
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
                'games': row['games']
            }
            _append(match_data)

        # if row['sport_name'] == 'Football':
             #match_data['scoreboard'] = generate_football_scoreboard(row)
        return markets_queue

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
        markets_to_send = self.generate_live_fixtures(res)
        resolved_live = self.resolve_game(res)
        resolved_to_send=[live for live in resolved_live if live["games"]]

        return markets_to_send, resolved_to_send

    def resolve_game(self,data: List[Dict]) -> List[Dict]:

        resolved_queue=list()
        _append=resolved_queue.append
        for row in data:
            fixture_proccessed_live = {
                "source": "neofeed_live_3",
                "fixtureId": row['ItemID'],
                "games": []
            }
            if row['sport'] =='Football':
                fixture_proccessed_live['games'] = resolve_football(row,self.redis_result,self.redis_market)

            _append(fixture_proccessed_live)
        return resolved_queue

