import os
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

from_number = os.environ["TWILIO_FROM_NUMBER"]
to_number = os.environ["TWILIO_TO_NUMBER"]

def send_message(text):
    # Append a friendly emoji to all outgoing SMS messages
    text_with_emoji = f"{text} 🙂"
    message = client.messages \
                .create(
                    body=text_with_emoji,
                    from_=from_number,
                    to=to_number
                )

    print(message.sid)