import os
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

from_number = os.environ["TWILIO_FROM_NUMBER"]
to_number = os.environ["TWILIO_TO_NUMBER"]

def _get_bool_env(var_name: str, default: bool = False) -> bool:
    value = os.environ.get(var_name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in ("1", "true", "yes", "on"):  # enabled
        return True
    if normalized in ("0", "false", "no", "off"):  # disabled
        return False
    return default

def send_message(text):
    # Optionally append an emoji to outgoing SMS messages, controlled via env
    append_emoji = _get_bool_env("SMS_APPEND_EMOJI", default=True)
    configured_emoji = os.environ.get("SMS_EMOJI", "🙂")

    if append_emoji and configured_emoji:
        text_to_send = f"{text} {configured_emoji}"
    else:
        text_to_send = text
    message = client.messages \
                .create(
                    body=text_to_send,
                    from_=from_number,
                    to=to_number
                )

    print(message.sid)