from time import time
from typing import Dict, List,AnyStr
import pandas as pd
import json
from dataclasses import dataclass,field
from os import getenv
from dotenv import load_dotenv
from utils.markets_editor import *

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
        formatted_data = {"ItemID": 0, "TournamentId": 0, "TournamentName": 0, "country_id": 0, "country_name": 0,
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
                        formatted_data["ItemID"] = _int(games[l]["id"])
                        formatted_data["event_start_time"] = _int(games[l]["start_ts"])
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
                                if formatted_data["event_period"]=="finished":
                                    print(formatted_data["ItemID"],"FINISHED")
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
            else cond in case new arrived data have no corensponing itemid in redis, we need to assign to it some value(event_score) to old_score in order
            to prevent old_score to remain 0 and cause errors with resolving. 
            """
            for i in queue:
                for j in old_result:
                    if j["ItemID"] == i["ItemID"]:
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

        formatted_data = {"OddsTypeName": 0, "quote": 0, "sourceGameId": 0, "ItemID": 0, "locked": 0,
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
                formatted_data["ItemID"] = _int(game[j]["id"])
                _id = formatted_data["ItemID"]
                list_raw_data = {_id: _list()}
                if game[j]["market"]:
                    formatted_data["locked"] = False
                    # formatted_data["timestamp"] = _int(time())
                    raw_data = game[j]["market"]
                    for k in raw_data:
                        base = raw_data[k]["base"] if "base" in raw_data[k] else ""
                        formatted_data["sourceGameId"] = _int(k)
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

                    unpacked_old_markets=[j for i in old_dict for j in i if j["ItemID"]==_id]
                    for i in unpacked_old_markets:
                        i["locked"]=True
                    list_raw_data = {_id: unpacked_old_markets}
                    _append(list_raw_data)

        return queue

    def fill_missing_data_keys(self, data: List[Dict],random_ids_list,miss_keys_redis) -> List[Dict]:
        """
        Fills missing data keys values using rotating pool of random list of nums that are unique and persistant for every team;
        teams ids are saved in redis as well as in json file as backup if redis go down;
        e.g missing keys home_id,away_id...;
        """
        _int=int
        load_from_redis=miss_keys_redis.load_missing_keys()
        if load_from_redis:
            existing_teams=[i["name"] for i in load_from_redis]
        else:
            existing_teams=[]

        arrived_team_names=list()
        for i in data:
            arrived_team_names.extend([i["home_name"],i["away_name"]])
        """
        unmapped_teams are teams that are not in redis but are only in arrived data
        """
        # existing_teams=[i["name"] for i in load_from_redis]
        unmapped_teams=list(set(arrived_team_names) - set(existing_teams))
        if not unmapped_teams:
            for i in data:
                for j in load_from_redis:
                    if j["name"] == i["home_name"]:
                        i["home_id"]=j["id"]
                    elif j["name"]== i["away_name"]:
                        i["away_id"]=j["id"]
        else:
            len_unmapped_teams=len(unmapped_teams)
            """
            to prevent duplicates teams ids in every else condition we pop out used ids and remained ids we write to csv file ids_random.csv.
            Then we make pairs from unmapped_tams and popped ids and proceed to populate missing data. 
            """
            ids=[random_ids_list.pop(-1) for i in range(len_unmapped_teams)]
            pd.DataFrame(random_ids_list).to_csv(self.ids_random_path,index=False,header=False)
            pairs=list(zip(unmapped_teams,ids))
            id_name=[{"name":i[0], "id":i[1]} for i in pairs]

            """
            adding a backup as file-like object if redis goes down
            discus with others if its necessary this step
            """
            with open(self.miss_teams, 'w') as outfile:
                json.dump(load_from_redis, outfile)
            miss_keys_redis.save_missing_keys(id_name)

            for i in data:
                for j in id_name:
                    if j["name"] == i["home_name"]:
                        i["home_id"]=j["id"]
                        break
                    elif j["name"]== i["away_name"]:
                        i["away_id"]=j["id"]
                        break

        return data
