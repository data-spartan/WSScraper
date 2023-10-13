import re
import time
from dataclasses import dataclass,field
from utils.redis_hash import *
from utils.sports.football import FootballResolver
from os import getenv
from dotenv import load_dotenv,find_dotenv
from utils.log_func import *
from utils.queue import Queue, ResolvingQueue
@dataclass
class ResolverAdapter:
    load_dotenv(find_dotenv(".env.production"))

    results_hash: RedisHash = field(default=None, repr=False)
    markets_hash: RedisHash = field(default=None, repr=False)
    results_history_list: RedisHash = field(default=None, repr=False)
    resolved_queue: ResolvingQueue = field(default_factory=ResolvingQueue, repr=False)
    
    def __post_init__(self):
        self.re_split =re.split
        self.re_colon_dash = re.compile(r"[:-]")
        self.re_colon = re.compile(r"[:]")
        self.logg = logging_func("resolver_adapter", getenv("sender_logs"))[1]


    def resolve_football(self,row):
        competitor_1_overtime1_result=competitor_2_overtime1_result=competitor_1_overtime2_result = \
        competitor_2_overtime2_result=competitor_1_penalties_result=competitor_2_penalties_result= \
        competitor_1_overtime1_old_result=competitor_2_overtime1_old_result=competitor_1_overtime2_old_result= \
        competitor_2_overtime2_old_result=competitor_1_penalties_old_result=competitor_2_penalties_old_result=None
        try:
            if len(row['event_score'].split("-")) > 1:
                competitor_1_result,\
                competitor_2_result,\
                competitor_1_period_1_result,\
                competitor_2_period_1_result,\
                competitor_1_period_2_result,\
                competitor_2_period_2_result, *overtime = list(map(int,re.split(pattern=r"[,:-]", string=row["event_score"])))
                if overtime:
                    if len(overtime)==2:
                        competitor_1_overtime1_result,competitor_2_overtime1_result=overtime
                    elif len(overtime)==4:
                        competitor_1_overtime1_result,competitor_2_overtime1_result,competitor_1_overtime2_result,competitor_2_overtime2_result=overtime
                    elif len(overtime)==6:
                        competitor_1_overtime1_result,competitor_2_overtime1_result,competitor_1_overtime2_result,competitor_2_overtime2_result,competitor_1_penalties_result,competitor_2_penalties_result=overtime

            else:
                competitor_1_result,\
                competitor_2_result,\
                competitor_1_period_1_result,\
                competitor_2_period_1_result = list(map(int,re.split(pattern=r"[,:-]", string=row["event_score"])))
                competitor_1_period_2_result, competitor_2_period_2_result = 0, 0

        except Exception as e:
            print(row)
            raise e
        try:
            if len(row['old_score'].split("-")) > 1:
                competitor_1_old_result,\
                competitor_2_old_result,\
                competitor_1_period_1_old_result, \
                competitor_2_period_1_old_result, \
                competitor_1_period_2_old_result, \
                competitor_2_period_2_old_result, *overtime =list(map(int,re.split(pattern=r"[,:-]", string=row["old_score"])))
                if overtime:
                    if len(overtime)==2:
                        competitor_1_overtime1_old_result,competitor_2_overtime1_old_result=overtime
                    elif len(overtime)==4:
                        competitor_1_overtime1_old_result,competitor_2_overtime1_old_result,competitor_1_overtime2_old_result,competitor_2_overtime2_old_result=overtime
                    elif len(overtime)==6:
                        competitor_1_overtime1_old_result,competitor_2_overtime1_old_result,competitor_1_overtime2_old_result,competitor_2_overtime2_old_result,competitor_1_penalties_old_result,competitor_2_penalties_old_result=overtime

            else:
                competitor_1_old_result,\
                competitor_2_old_result,\
                competitor_1_period_1_old_result,\
                competitor_2_period_1_old_result =list(map(int,re.split(pattern=r"[,:-]", string=row["old_score"])))
                competitor_1_period_2_old_result, competitor_2_period_2_old_result = 0, 0
        except Exception as e:
            print(row["ItemID"],row["old_score"],row["event_period"])
            raise e

        res = FootballResolver(
            competitor_1_result=competitor_1_result,
            competitor_2_result=competitor_2_result,
            competitor_1_period_1_result=competitor_1_period_1_result,
            competitor_2_period_1_result=competitor_2_period_1_result,
            competitor_1_period_2_result=competitor_1_period_2_result,
            competitor_2_period_2_result=competitor_2_period_2_result,
            competitor_1_overtime1_result=competitor_1_overtime1_result,
            competitor_2_overtime1_result=competitor_2_overtime1_result,
            competitor_1_overtime2_result=competitor_1_overtime2_result,
            competitor_2_overtime2_result=competitor_2_overtime2_result,
            competitor_1_penalties_result=competitor_1_penalties_result,
            competitor_2_penalties_result=competitor_2_penalties_result,
            competitor_1_old_result=competitor_1_old_result,
            competitor_2_old_result=competitor_2_old_result,
            competitor_1_period_1_old_result=competitor_1_period_1_old_result,
            competitor_2_period_1_old_result=competitor_2_period_1_old_result,
            competitor_1_period_2_old_result=competitor_1_period_2_old_result,
            competitor_2_period_2_old_result=competitor_2_period_2_old_result,
            competitor_1_overtime1_old_result=competitor_1_overtime1_old_result,
            competitor_2_overtime1_old_result=competitor_2_overtime1_old_result,
            competitor_1_overtime2_old_result=competitor_1_overtime2_old_result,
            competitor_2_overtime2_old_result=competitor_2_overtime2_old_result,
            competitor_1_penalties_old_result=competitor_1_penalties_old_result,
            competitor_2_penalties_old_result=competitor_2_penalties_old_result,
            corners=sum(row["stats"]["corner"]) if row["stats"]["corner"] else 0,
            yellow_cards_comp1=row["stats"]["yellow_card"][0] if row["stats"]["yellow_card"] else 0,
            yellow_cards_comp2=row["stats"]["yellow_card"][1] if row["stats"]["yellow_card"] else 0,
            red_cards_comp1=row["stats"]["red_card"][0] if row["stats"]["red_card"] else 0,
            red_cards_comp2=row["stats"]["red_card"][1] if row["stats"]["red_card"] else 0,
            period=row['event_period'],
            match_minutes=row['event_seconds'],
            resolving_queue=self.resolved_queue)
        
        statistics_dict= {attr: getattr(res, attr) for attr in dir(res) if not callable(getattr(res, attr)) and not attr.startswith("__") and 'old' not in attr and attr != 'resolving_queue'}
        res.run_games()
        # print(res.get_data())
        return res.get_data(),statistics_dict
        # return resolved_games

