
def football_markets_formatter(formatted_data,events):
    """
    formats some group of markets that have non-adequate info or missing keys
    e.g. correct score market for key "type" gives Away-Home, but for key "name" give 3-1 and many other markets
    """
    if "Score/Match score" in formatted_data or "Correct Score" in formatted_data:
        sub_type = events["name"]
    elif "type" in events and "Correct Score" not in formatted_data:
        sub_type = events["type"]
    elif "type_1" in events and "Correct Score" not in formatted_data:
        sub_type = events["type_1"]
    else:
        sub_type=events["name"]
    return sub_type
