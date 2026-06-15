def get_position():
    try:
        from SimConnect import SimConnect, AircraftRequests
        sm = SimConnect()
        aq = AircraftRequests(sm, _time=0)
        lat = aq.get("PLANE_LATITUDE")
        lon = aq.get("PLANE_LONGITUDE")
        if lat is None or lon is None:
            return None
        return {"lat": float(lat), "lon": float(lon)}
    except Exception:
        return None
