import requests

VATSIM_URL = "https://data.vatsim.net/v3/vatsim-data.json"

def get_atc():
    try:
        data = requests.get(VATSIM_URL, timeout=10).json()

        controllers = []

        for c in data.get("controllers", []):
            if not c.get("callsign"):
                continue

            controllers.append({
                "callsign": c.get("callsign"),
                "frequency": c.get("frequency", "N/A"),
                "name": c.get("name"),
                "lat": c.get("latitude"),
                "lon": c.get("longitude"),
            })

        return controllers

    except Exception as e:
        print("[VATSIM ERROR]", e)
        return []
