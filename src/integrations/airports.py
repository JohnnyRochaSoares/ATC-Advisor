import os
import json
import time
import requests

AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
CACHE_FILE = os.path.join(os.path.dirname(__file__), "airports_cache.json")
CACHE_TTL = 86400

def _cache_valid():
    if not os.path.exists(CACHE_FILE):
        return False
    return (time.time() - os.path.getmtime(CACHE_FILE)) < CACHE_TTL

def _download_airports():
    response = requests.get(AIRPORTS_URL, timeout=30)
    response.raise_for_status()

    airports = {}
    lines = response.text.splitlines()

    # Remove aspas dos headers
    headers = [h.strip().strip('"') for h in lines[0].split(",")]

    idx_icao = headers.index("ident")
    idx_lat  = headers.index("latitude_deg")
    idx_lon  = headers.index("longitude_deg")
    idx_type = headers.index("type")

    for line in lines[1:]:
        parts = line.split(",")
        if len(parts) <= max(idx_icao, idx_lat, idx_lon):
            continue

        icao = parts[idx_icao].strip().strip('"')
        kind = parts[idx_type].strip().strip('"')

        if not icao or len(icao) != 4:
            continue
        if kind not in ("large_airport", "medium_airport", "small_airport"):
            continue

        try:
            airports[icao] = {
                "lat": float(parts[idx_lat].strip().strip('"')),
                "lon": float(parts[idx_lon].strip().strip('"')),
            }
        except ValueError:
            continue

    with open(CACHE_FILE, "w") as f:
        json.dump(airports, f)

    return airports

def get_airports():
    if _cache_valid():
        with open(CACHE_FILE) as f:
            return json.load(f)
    try:
        return _download_airports()
    except Exception as e:
        print("[AIRPORTS ERROR]", e)
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE) as f:
                return json.load(f)
        return {}
