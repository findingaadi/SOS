import os
from dotenv import load_dotenv
load_dotenv()

AWS_REGION_DDB = os.getenv("AWS_REGION_DDB", "eu-north-1")
DDB_TABLE      = os.getenv("DDB_TABLE", "earthquake_subscribers")
COOLDOWN_SECONDS = int(os.getenv("COOLDOWN_SECONDS", "300"))

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN  = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM        = os.getenv("TWILIO_FROM", "")

