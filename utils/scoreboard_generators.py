import copy
from constants import *
from time import time
import re
def generate_fixture_with_one_value(setting_value) -> dict:
    return {'110':setting_value , '111': setting_value, '112': setting_value}

def generate_football_scoreboard(row: dict) -> dict:
    raw = {'corners_home_p1':0, 'corners_away_p1':0, 'corners_home_p2':0, 'corners_away_p2':0,\
            'substitutions_home_p1':0, 'substitutions_away_p1':0, 'substitutions_home_p2':0, 'substitutions_away_p2':0,\
            'red_cards_home_p1':0, 'red_cards_away_p1':0, 'red_cards_home_p2':0, 'red_cards_away_p2':0,\
            'yellow_cards_home_p1':0, 'yellow_cards_away_p1':0, 'yellow_cards_home_p2':0, 'yellow_cards_away_p2':0}
    if len(row['event_score'].split("-")) > 1:
        try:
            c1_p1, c2_p1, c1_p2, c2_p2, *overtime = [int(sub) if sub !='' else 0 for sub in (re.split(pattern=r"[:-]", string=row['event_score']))]
        except Exception as e:
            c1_p1, c2_p1, c1_p2, c2_p2 = 0,0,0,0
    else:
        try:
            c1_p1, c2_p1 = [int(sub) if sub !='' else 0 for sub in (re.split(pattern=r"[:]", string=row['event_score']))]
        except Exception as e:
            c1_p1, c2_p1 = 0, 0
        c1_p2, c2_p2 = 0, 0

    raw.update(row)
    row = raw
    visible = 1
    running = 1
    if row['event_seconds'] == "Ended" or row['event_seconds'] == "HT" or row['event_seconds'] == "Paused":
        running = 0
        visible = 0
        row['event_period'] = row['event_seconds']
        row['event_seconds'] = 0
    else:
        if not isinstance(row['event_seconds'], str):
            delay_offset = int(time()) - int(row['event_fetched_timestamp'])
            row['event_seconds'] = int(row['event_seconds']) + delay_offset
        else:
            row['event_seconds'] = 0

    data = { 
        'corners': {
            'c1': {'110': int(row['corners_home_p1']), '111': int(row['corners_home_p2']), '112': int(row['corners_home_p1']) + int(row['corners_home_p2'])} ,
            'c2':{'110': int(row['corners_away_p1']), '111': int(row['corners_away_p2']), '112': int(row['corners_away_p1']) + int(row['corners_away_p2'])}
        },
        'redCards': {
            'c1': {'110': int(row['red_cards_home_p1']), '111': int(row['red_cards_home_p2']), '112': int(row['red_cards_home_p1']) + int(row['red_cards_home_p2'])} ,
            'c2':{'110': int(row['red_cards_away_p1']), '111': int(row['red_cards_away_p2']), '112': int(row['red_cards_away_p1']) + int(row['red_cards_away_p2'])}
        },
        'yellowCards':{
            'c1': {'110': int(row['yellow_cards_home_p1']), '111': int(row['yellow_cards_home_p2']), '112': int(row['yellow_cards_home_p1']) + int(row['yellow_cards_home_p2'])} ,
            'c2':{'110': int(row['yellow_cards_away_p1']), '111': int(row['yellow_cards_away_p2']), '112': int(row['yellow_cards_away_p1']) + int(row['yellow_cards_away_p2'])}
        },
        'offsides': {'c1':generate_fixture_with_one_value(0), 'c2':generate_fixture_with_one_value(0)},
        'throwIns': {'c1':generate_fixture_with_one_value(0), 'c2':generate_fixture_with_one_value(0)},
        'penalties': {'c1': generate_fixture_with_one_value(0) ,'c2':generate_fixture_with_one_value(0)},
        'substitutions':  {
            'c1': {'110': int(row['substitutions_home_p1']), '111': int(row['substitutions_home_p2']), '112': int(row['substitutions_home_p1']) + int(row['substitutions_home_p2'])} ,
            'c2':{'110': int(row['substitutions_away_p1']), '111': int(row['substitutions_away_p2']), '112': int(row['substitutions_away_p1']) + int(row['substitutions_away_p2'])}
        },
        'goalKicks':  {'c1': generate_fixture_with_one_value(0) ,'c2':generate_fixture_with_one_value(0)},
        'freeKicks':  {'c1': generate_fixture_with_one_value(0) ,'c2':generate_fixture_with_one_value(0)},
        'score':  {
            'c1': {'110': int(c1_p1), '111': int(c1_p2), '112':int(c1_p1 + c1_p2)}, 
            'c2': {'110': int(c2_p1), '111': int(c2_p2), '112':int(c2_p1 + c2_p2)}
        },
        'periodId': str(row['event_period']) if str(row['event_period']) in football_periods_translation.keys() else row['event_period'],
        'availablePeriods': [],
        'messages': [],
        'timer': {'visible': visible, 'running': running, 'seconds': row['event_seconds'], 'refTimestamps': int(row['event_fetched_timestamp'])}
    }
    return data


