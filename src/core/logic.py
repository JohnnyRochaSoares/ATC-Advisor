from core.distance import distance_nm
from integrations.airports import get_airports

_airports = None

def _get_airports_cached():
    global _airports
    if _airports is None:
        _airports = get_airports()
    return _airports

def get_atc_position(callsign):
    airports = _get_airports_cached()
    for length in (4, 3, 2):
        prefix = callsign[:length].upper()
        if prefix in airports:
            return airports[prefix]
    return None

def find_nearest_atc(position, atc_list):
    nearest = None
    min_dist = float("inf")

    for c in atc_list:
        pos = get_atc_position(c["callsign"])
        if pos is None:
            continue

        d = distance_nm(position["lat"], position["lon"], pos["lat"], pos["lon"])
        c["distance_nm"] = round(d, 1)

        if d < min_dist:
            min_dist = d
            nearest = c

    return nearest

def should_alert(atc, alert_distance_nm: float) -> bool:
    return atc.get("distance_nm", float("inf")) <= alert_distance_nm
