import re, logging
from twilio.rest import Client as TwilioClient
from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM

E164_RE = re.compile(r"^\+\d{7,15}$")
_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN) else None

def call(phone_e164: str, tts_message: str) -> bool:
    if not _client:
        logging.warning("Twilio not configured; skip call to %s", phone_e164); return False
    if not E164_RE.match(phone_e164):
        logging.warning("Twilio call invalid E.164: %s", phone_e164); return False
    try:
        twiml = f'<Response><Say voice="alice">{tts_message}</Say></Response>'
        c = _client.calls.create(to=phone_e164, from_=TWILIO_FROM, twiml=twiml)
        logging.info("Twilio call SID %s to %s", c.sid, phone_e164); return True
    except Exception:
        logging.exception("Twilio call failed to %s", phone_e164); return False