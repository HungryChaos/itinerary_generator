# services/opentripmap.py
import os, requests
API_KEY = os.getenv("OPENTRIPMAP_KEY")
BASE = "https://api.opentripmap.com/0.1/en/places"

def get_pois(lat, lon, kinds="cultural,museums,food", radius=2000, limit=50):
    url = f"{BASE}/radius"
    params = {"apikey": API_KEY, "lat": lat, "lon": lon, "radius": radius, "kinds": kinds, "limit": limit}
    r = requests.get(url, params=params)
    return r.json()
