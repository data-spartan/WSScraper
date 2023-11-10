from time import time
from typing import Dict, List,AnyStr
import pandas as pd
import json
import uuid
from dataclasses import dataclass,field
from os import getenv
from dotenv import load_dotenv
from utils.markets_editor import *
import hashlib

load_dotenv(".env")

@dataclass
class Parsers:
    miss_teams: AnyStr = field(default_factory=lambda: getenv("missing_team_names"),repr=False)
    ids_random_path: AnyStr = field(default_factory=lambda: getenv("ids_random_path"),repr=False)


    def match_info_parser(self,raw_data: Dict, old_result: List[Dict]) -> List[Dict]:
        """
        Parsing and formatting match info data;
        e.g. score, tournament, stats ...;
        """
        formatted_data = {"ItemId": 0, "TournamentId": 0, "TournamentName": 0, "country_id": 0, "country_name": 0,
                          "sport_id": 0, "sport": 0, "home_id": 0, "away_id": 0,"home_name": 0, "away_name": 0, "event_score": 0, "old_score":0,
                          "event_seconds": 0, "event_start_time": 0, "event_fetched_timestamp": 0, "event_period": 0,"stats":{
                          "goal_kick": 0, "corner":0, "foul":0,"yellow_card": 0, "red_card":0,'free_kick':0,"injuries":0, "substitutions":0}}
        queue = list()
        """
        using func references in loops, bcs it gives perf boost cca 5%
        """
        _append = queue.append
        _int = int
        _list = list
        _dict = dict

        formatted_data["event_fetched_timestamp"] = _int(time())
        for i in raw_data:
            formatted_data["sport"] = raw_data[i]["name"]
            formatted_data["sport_id"] = _int(i)
            region = raw_data[i]['region']
            for j in region:
                formatted_data['country_id'] = _int(region[j]["id"])
                formatted_data['country_name'] = region[j]["name"]
                competition = region[j]["competition"]
                for k in competition:
                    formatted_data["TournamentId"] = _int(competition[k]["id"])
                    formatted_data["TournamentName"] = competition[k]["name"]
                    games = competition[k]["game"]
                    for l in games:
                        """
                        sometimes happens some matches dont event start but we get them in payload without many data keys, so scraper breaks.
                        more interestignly sometimes we get matches that are in progress but with missing keys, so we just skip those mathches until we get appropriete
                        payload for these matcehs.
                        """
                        if ("current_game_state" in games[l]["info"]) and (not games[l]["info"]["current_game_state"] == "notstarted") and ("score_set1" in games[l]["stats"]):
                            formatted_data["event_period"] = games[l]["info"]["current_game_state"]
                        else:
                            continue
                        formatted_data["ItemId"] = _int(games[l]["id"])
                        
                        if "start_ts" in games[l]:
                            formatted_data["event_start_time"] = _int(games[l]["start_ts"])
                        else:
                            old_start_time = list(filter(lambda x: x["ItemId"]==formatted_data["ItemId"], old_result))
                            start_time=old_start_time[0]["event_start_time"] if old_start_time else None
                            formatted_data["event_start_time"] = start_time
                            

                        #sometimes when match is finished there is no start time proeprty in feed
                        formatted_data["home_name"] = games[l]["team1_name"]
                        formatted_data["away_name"] = games[l]["team2_name"]

                        if formatted_data["sport"] == "Football":
                            """
                            when ht is on, there are no stats such as goal,score_set2,current_game_time..
                            """
                            if formatted_data["event_period"] in ["set1","Half Time","timeout"]:
                                """
                                using f-string represantion for formatting match score instead of conventional score data formatting(using str methods,map, slicing...)
                                increases parsing performance for outstanding cca 270%      
                                """
                                formatted_data["event_score"] = f'{games[l]["info"]["score1"]}:{games[l]["info"]["score2"]},{games[l]["stats"]["score_set1"]["team1_value"]}:{games[l]["stats"]["score_set1"]["team2_value"]}'
                                formatted_data["event_seconds"] = games[l]["info"]["current_game_time"] if formatted_data["event_period"] =="set1" else formatted_data["event_period"]
                                formatted_data["event_period"] = "1" if formatted_data["event_period"] =="set1" else formatted_data["event_period"]

                            elif formatted_data["event_period"] == "set2":
                                formatted_data["event_score"] = f'{games[l]["info"]["score1"]}:{games[l]["info"]["score2"]},{games[l]["stats"]["score_set1"]["team1_value"]}:{games[l]["stats"]["score_set1"]["team2_value"]}-{games[l]["stats"]["score_set2"]["team1_value"]}:{games[l]["stats"]["score_set2"]["team2_value"]}'
                                formatted_data["event_seconds"] = games[l]["info"]["current_game_time"]
                                formatted_data["event_period"] = "2"

                            elif formatted_data["event_period"] == "finished":
                                formatted_data["event_period"] = "Ended"
                                formatted_data["event_seconds"] = "Ended"
                                print(formatted_data["ItemId"],"Ended")
                                for scores in games[l]["stats"]:
                                    """
                                    excluding set3 bcs game cant be finished in overtime1(extra-time) period
                                    """
                                    if scores == "score_set2":
                                        formatted_data["event_score"] = f'{games[l]["info"]["score1"]}:{games[l]["info"]["score2"]},{games[l]["stats"]["score_set1"]["team1_value"]}:{games[l]["stats"]["score_set1"]["team2_value"]}-{games[l]["stats"]["score_set2"]["team1_value"]}:{games[l]["stats"]["score_set2"]["team2_value"]}'
                                    elif scores == "score_set4":
                                        formatted_data["event_score"] = f'{games[l]["info"]["score1"]}:{games[l]["info"]["score2"]},{games[l]["stats"]["score_set1"]["team1_value"]}:{games[l]["stats"]["score_set1"]["team2_value"]}-{games[l]["stats"]["score_set2"]["team1_value"]}:{games[l]["stats"]["score_set2"]["team2_value"]}-{games[l]["stats"]["score_set3"]["team1_value"]}:{games[l]["stats"]["score_set3"]["team2_value"]}-{games[l]["stats"]["score_set4"]["team1_value"]}:{games[l]["stats"]["score_set4"]["team2_value"]}'
                                    elif scores == "score_set5":
                                        formatted_data["event_score"] = f'{games[l]["info"]["score1"]}:{games[l]["info"]["score2"]},{games[l]["stats"]["score_set1"]["team1_value"]}:{games[l]["stats"]["score_set1"]["team2_value"]}-{games[l]["stats"]["score_set2"]["team1_value"]}:{games[l]["stats"]["score_set2"]["team2_value"]}-{games[l]["stats"]["score_set3"]["team1_value"]}:{games[l]["stats"]["score_set3"]["team2_value"]}-{games[l]["stats"]["score_set4"]["team1_value"]}:{games[l]["stats"]["score_set4"]["team2_value"]}-{games[l]["stats"]["score_set5"]["team1_value"]}:{games[l]["stats"]["score_set5"]["team2_value"]}'

                            elif formatted_data["event_period"] == "set3":
                                formatted_data["event_score"] = f'{games[l]["info"]["score1"]}:{games[l]["info"]["score2"]},{games[l]["stats"]["score_set1"]["team1_value"]}:{games[l]["stats"]["score_set1"]["team2_value"]}-{games[l]["stats"]["score_set2"]["team1_value"]}:{games[l]["stats"]["score_set2"]["team2_value"]}-{games[l]["stats"]["score_set3"]["team1_value"]}:{games[l]["stats"]["score_set3"]["team2_value"]}'
                                formatted_data["event_seconds"] = games[l]["info"]["current_game_time"]
                                formatted_data["event_period"] = "overtime1" ##extra-time-1

                            elif formatted_data["event_period"] == "set4":
                                formatted_data["event_score"] = f'{games[l]["info"]["score1"]}:{games[l]["info"]["score2"]},{games[l]["stats"]["score_set1"]["team1_value"]}:{games[l]["stats"]["score_set1"]["team2_value"]}-{games[l]["stats"]["score_set2"]["team1_value"]}:{games[l]["stats"]["score_set2"]["team2_value"]}-{games[l]["stats"]["score_set3"]["team1_value"]}:{games[l]["stats"]["score_set3"]["team2_value"]}-{games[l]["stats"]["score_set4"]["team1_value"]}:{games[l]["stats"]["score_set4"]["team2_value"]}'
                                formatted_data["event_seconds"] = games[l]["info"]["current_game_time"]
                                formatted_data["event_period"] = "overtime2"

                            elif formatted_data["event_period"] == "set5":
                                formatted_data["event_score"] = f'{games[l]["info"]["score1"]}:{games[l]["info"]["score2"]},{games[l]["stats"]["score_set1"]["team1_value"]}:{games[l]["stats"]["score_set1"]["team2_value"]}-{games[l]["stats"]["score_set2"]["team1_value"]}:{games[l]["stats"]["score_set2"]["team2_value"]}-{games[l]["stats"]["score_set3"]["team1_value"]}:{games[l]["stats"]["score_set3"]["team2_value"]}-{games[l]["stats"]["score_set4"]["team1_value"]}:{games[l]["stats"]["score_set4"]["team2_value"]}-{games[l]["stats"]["score_set5"]["team1_value"]}:{games[l]["stats"]["score_set5"]["team2_value"]}'
                                formatted_data["event_seconds"] = games[l]["info"]["current_game_time"]
                                formatted_data["event_period"] = "penalties"

                        for stat in list(set(formatted_data["stats"]) & set(games[l]["stats"])):
                            """
                            Using dict intersection between formatted_data and arrived data stats keys to filter out only existent ones in order to
                            avoid Key error as well as try;except statement which is performance costly.
                            """
                            formatted_data["stats"][stat]=games[l]["stats"][stat]["team1_value"],games[l]["stats"][stat]["team2_value"]

                        _append(formatted_data)
                        """
                        after each iteration we need to create new dict object to ensure that every match has
                        unique formatted_data data structure when populating it.
                        """
                        formatted_data = _dict(formatted_data)
        if old_result:
            """
            adding old_score to the newly arrived results;if first time arrived data then add event_score to old_score;
            else cond in case new arrived data have no corensponing ItemId in redis, we need to assign to it some value(event_score) to old_score in order
            to prevent old_score to remain 0 and cause errors with resolving. 
            """
            for i in queue:
                for j in old_result:
                    if j["ItemId"] == i["ItemId"]:
                        i["old_score"]=j["event_score"]
                        break
                    else:
                        i["old_score"]=i["event_score"]
        else:
            for i in queue:
                i["old_score"]=i["event_score"]
        return queue

    def markets_parser(self,raw_data: dict, old_dict: dict) -> dict:
        """
        Parsing and formatting markets data;
        e.g. games, quotes...;
        """

        formatted_data = {"OddsTypeName": 0, "quote": 0, "sourceGameId": 0, "ItemId": 0, "locked": 0,
                          "type": 0}##deleted timestamp, discus if necessary
        queue = list()
        _append = queue.append
        _list = list
        _dict = dict
        _int=int
        for i in raw_data:
            sport_id=raw_data[i]["id"]
            game = raw_data[i]["game"]
            for j in game:
                formatted_data["ItemId"] = _int(game[j]["id"])
                _id = formatted_data["ItemId"]
                list_raw_data = {_id: _list()}
                if game[j]["market"]:
                    formatted_data["locked"] = False
                    # formatted_data["timestamp"] = _int(time())
                    raw_data = game[j]["market"]
                    for k in raw_data:
                        base = raw_data[k]["base"] if "base" in raw_data[k] else ""
                        # formatted_data["sourceGameId"] = _int(k)
                        formatted_data["OddsTypeName"] = raw_data[k]["name"]
                        events = raw_data[k]["event"]
                        for l in events:
                            formatted_data["quote"] = events[l]["price"]
                            if sport_id == 1: ###FOTBALL
                                """
                                Skip this market, no way to resolve any Goalscorer markets
                                """
                                if "Goalscorer" in formatted_data["OddsTypeName"]:
                                    break
                                else:
                                    sub_type=football_markets_formatter(formatted_data["OddsTypeName"],events[l])
                            if base == "":
                                formatted_data["type"] = f'{formatted_data["OddsTypeName"]}|{sub_type.strip()}'
                            else:
                                formatted_data["type"] = f'{formatted_data["OddsTypeName"]} {base}|{sub_type.strip()}'
                            # print(f"{k}{sub_type.strip()}")
                            formatted_data["sourceGameId"] = 0 #f"{k}{sub_type.strip()}"
                            list_raw_data[_id].append(formatted_data)
                            """
                            after each iteration we need to create new dict object to ensure that every market has
                            unique formatted_data data structure when populating it.
                            """
                            formatted_data = _dict(formatted_data)

                    _append(list_raw_data)
                else:
                    """
                    else statement fires when game[j]["market"] is empty, it means that match markets are locked,
                    so we use previous non blocked entry from redis but with varibale "locked"=true to send on COU. 
                    """

                    unpacked_old_markets=[j for i in old_dict for j in i if j["ItemId"]==_id]
                    for i in unpacked_old_markets:
                        i["locked"]=True
                    list_raw_data = {_id: unpacked_old_markets}
                    _append(list_raw_data)

        return queue

    def fill_missing_teams_ids(self, data,existing_teams):
        #feed doesnt have team ids, i needed to generate them and persist them in redis to maintain data integrity
        new = {}
        for fixt in data:        
            if not existing_teams.get(fixt['home_name']):#if in redis id for specific team doesnt exist generate id
                hash1=uuid.uuid1().__str__()
                new.update({fixt['home_name']:hash1})
                fixt['home_id']=hash1
            else:
                home_id=existing_teams.get(fixt['home_name'])
                fixt['home_id']=home_id
            if not existing_teams.get(fixt['away_name']):
                hash2=uuid.uuid1().__str__()
                new.update({fixt['away_name']:hash2})
                fixt['away_id']=hash2
            else:
                away_id=existing_teams.get(fixt['away_name'])
                fixt['away_id']=away_id

            existing_teams.update(new)
        return data, new
            
    def fill_missing_markets_ids(self, data, existing_markets):
        #feed doesnt have team ids, i needed to generate them and persist them in redis to maintain data integrity
        new = {}
        for markets in data:        
            key=list(markets.keys())[0] #fixtureId
            for market in markets[key]:
                if not existing_markets.get(market['type']):#if in redis id for specific team doesnt exist generate id
                    hash_=uuid.uuid4().__str__()
                    new.update({market['type']:hash_})
                    market['sourceGameId']=hash_
                else:
                    market_id=existing_markets.get(market['type'])
                    market['sourceGameId']=market_id

        existing_markets.update(new)
        return data, new