import os
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

from_number = os.environ["TWILIO_FROM_NUMBER"]
to_number = os.environ["TWILIO_TO_NUMBER"]

message = client.messages \
            .create(
                body="test",
                from_=from_number,
                to=to_number
            )