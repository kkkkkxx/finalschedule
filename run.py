# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Find these values at https://twilio.com/user/account
account_sid = "AC8d3cd606442775ed86d1e6cd26f3cd43"
auth_token = "457ee4916f5c5ed892e83dc37c924b45"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(to="+4124179805", from_="+14122534757",
                                     body="Hello there!!!")
