from __future__ import unicode_literals

from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop
from tornado import gen

import logging, json, sys
from app.config import COOLDOWN_SECONDS
from app.geo import haversine
from app.cooldown import Cooldown
from app.storage import scan_subscribers
from app.notifier_twilio import call as twilio_call

ECHO_URI = 'wss://www.seismicportal.eu/standing_order/websocket'
PING_INTERVAL = 15

processed_quakes = set()
cooldown_call = Cooldown(COOLDOWN_SECONDS)

def format_alert_text(user_name, mag, region, time_str, distance_km):
    mag_txt  = f"M{mag}" if mag is not None else "Magnitude unknown"
    dist_txt = f"{distance_km:.1f} km away" if distance_km is not None else ""
    parts = [f"Earthquake alert for {user_name}:", f"{mag_txt} detected in {region} at {time_str}."]  # noqa
    if dist_txt: parts.append(dist_txt)
    parts.append("This is an automated notification.")
    return " ".join(parts)

def process_event(message):
    data  = json.loads(message)
    props = data['data']['properties']
    quake_id = props.get('unid')

    quake_lat = float(props['lat']); quake_lon = float(props['lon'])
    mag = props.get('mag', 0); region = props.get('flynn_region', 'Unknown')
    time_str = props.get('time')

    logging.info("Earthquake: %.1fM in %s at %s", mag, region, time_str)

    if quake_id and quake_id in processed_quakes:
        logging.info("Skip quake %s (already processed)", quake_id); return
    if quake_id: processed_quakes.add(quake_id)

    users = scan_subscribers()
    any_alert = False

    for u in users:
        distance = haversine(quake_lat, quake_lon, u["lat"], u["lon"])
        if distance <= u["radius"]:
            any_alert = True
            msg = format_alert_text(u["name"], mag, region, time_str, distance)

            key = f"call:{u.get('id') or u['number']}"
            if cooldown_call.allow(key):
                logging.info("Calling %s (%.1f km)", u["name"], distance)
                ok = twilio_call(u["number"], msg)
                if not ok: cooldown_call._last[key] = 0 
            else:
                logging.info("Skip call %s (cooldown %ds)", u["name"], cooldown_call.remaining(key))

    if not any_alert: logging.info("No nearby subscribers for this quake")

@gen.coroutine
def listen(ws):
    while True:
        msg = yield ws.read_message()
        if msg is None: logging.info("close"); break
        try: process_event(msg)
        except Exception: logging.exception("Error processing message")

@gen.coroutine
def launch_client():
    try:
        logging.info("Open WebSocket %s", ECHO_URI)
        ws = yield websocket_connect(ECHO_URI, ping_interval=PING_INTERVAL)
    except Exception:
        logging.exception("WebSocket connection error")
    else:
        logging.info("Waiting for messages..."); yield listen(ws)

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    IOLoop.instance().run_sync(launch_client)

if __name__ == "__main__": main()