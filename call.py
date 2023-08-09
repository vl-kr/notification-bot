# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure]

def dial():
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    call = client.calls.create(
                            twiml='<Response><Say>Ahoy, World!</Say></Response>',
                            to='+421xxxxxxxxx',
                            from_='+420xxxxxxxxx'
                        )
    print(call.sid)
