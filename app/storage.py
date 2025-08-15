import json, boto3
from app.config import AWS_REGION_DDB, DDB_TABLE

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION_DDB)
table = dynamodb.Table(DDB_TABLE)

def normalize_user_item(item):
    loc_raw = item.get('location')
    if isinstance(loc_raw, str):
        try: loc = json.loads(loc_raw)
        except Exception: return None
    else:
        loc = loc_raw or {}
    lat_field = loc.get('lat'); lon_field = loc.get('lon')
    if lat_field is None or lon_field is None: return None

    if isinstance(lat_field, dict):
        user_lat = float(lat_field.get('S')); user_lon = float(lon_field.get('S'))
    else:
        user_lat = float(lat_field); user_lon = float(lon_field)

    try: radius = float(item.get('radius', 0))
    except Exception: radius = 0.0

    return {
        "id": item.get("id"),
        "name": item.get("name", "user"),
        "number": item.get("number", ""),
        "radius": radius,
        "lat": user_lat,
        "lon": user_lon
    }

def scan_subscribers():
    items = table.scan().get("Items", [])
    return [u for it in items if (u := normalize_user_item(it))]