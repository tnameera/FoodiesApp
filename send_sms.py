import os
from twilio.rest import Client
from secrets import twilio_sid, twilio_auth


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = twilio_sid
auth_token = twilio_auth
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+18316099981',
                     to='+14254957671'
                 )

print(message.sid)
