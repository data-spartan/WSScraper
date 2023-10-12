import re
import time
from utils.redis_hash import *
from utils.sports.football import FootballResolver

def resolve_football(row,results_hash,markets_hash):
    competitor_1_overtime1_result=competitor_2_overtime1_result=competitor_1_overtime2_result = \
    competitor_2_overtime2_result=competitor_1_penalties_result=competitor_2_penalties_result= \
    competitor_1_overtime1_old_result=competitor_2_overtime1_old_result=competitor_1_overtime2_old_result= \
    competitor_2_overtime2_old_result=competitor_1_penalties_old_result=competitor_2_penalties_old_result=0
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
        period=row['event_period'])

    res.run_games()
    if row['event_period'] == "finished":
        results_hash.delete_key(row['ItemID'])
        markets_hash.delete_key(row['ItemID'])
    resolved_games = res.get_data()
    return resolved_games

