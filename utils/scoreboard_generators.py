import copy
from constants import *
from time import time
import re


def generate_football_scoreboard(stats: dict, time:str, period:str,fetched_timestamp:int) -> dict:
    
    visible = 1
    running = 1
    if time in ["finished","Half Time", "timeout"]:
        running = 0
        visible = 1
        period = time
        time=0
    else:
        if not isinstance(time, str):
            delay_offset = int(time()) - int(fetched_timestamp)
            time = int(time) + delay_offset
        else:
            time = 0

    
    data = { 
            'corners': {
                'corners':stats['corners']
            },
            'redCards': {
                'red_cards_comp1':stats['red_cards_comp1'],
                'red_cards_comp2':stats['red_cards_comp2']
            },
            'yellowCards':{
                'yellow_cards_comp1':stats['yellow_cards_comp1'],
                'yellow_cards_comp2':stats['yellow_cards_comp2']
            },
            'offsides': {},
            'throwIns': {},
            'penalties': {},
            'substitutions':  {
                
            },
            'goalKicks':  {},
            'freeKicks':  {},
            'score':  {
            'competitor_1_result':stats['competitor_1_result'],
            'competitor_2_result':stats['competitor_2_result']
            },
            'score_by_period':{
                'competitor_1_period_1_result':stats['competitor_1_period_1_result'],
                'competitor_2_period_1_result':stats['competitor_2_period_1_result'],
                'competitor_1_period_2_result':stats['competitor_1_period_2_result'],
                'competitor_2_period_2_result':stats['competitor_2_period_2_result'],
                'competitor_1_overtime1_result':stats['competitor_1_overtime1_result'],
                'competitor_2_overtime1_result':stats['competitor_2_overtime1_result'],
                'competitor_1_overtime2_result':stats['competitor_1_overtime2_result'],
                'competitor_2_overtime2_result':stats['competitor_2_overtime2_result'],
                'competitor_1_penalties_result':stats['competitor_1_penalties_result'],
                'competitor_2_penalties_result':stats['competitor_2_penalties_result']
            },
            'period': football_periods_translation[str(period)] if str(period) in football_periods_translation.keys() else period,
            'availablePeriods': [1,2], #1st,2nd half
            'timer': {'visible': visible, 'running': running, 'seconds': time, 'refTimestamps': fetched_timestamp}
        }
    
    
    
    return data


