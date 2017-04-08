from flask import Flask, request
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAAbCANkytUYBAHcOtp4HcKyJfKwdAX1X9NZCjLynZC26u0hSBvoDZAPDOIdmjf8GlcwUSCDn0eQjqfi3undSU6eFfHInckBHCLex8wG5oCsK0iwdOqT0vnKpDKBg0AMy0LOUlEkBGfzoy2iACjczPXBN3QHD0lD1UZB1hyXPygZDZD"


def send_message(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    print send(data)


def process_message(sender, text):
    greeting(sender)
    sendpic(sender)
    # words = text.split()
    # reply(sender, "tus palabras fueron: {}".format(words))
    send_button(sender)


@app.route('/', methods=['GET', 'POST'])
def handle_request():
    print request.method
    if request.method == 'GET':
        return handle_verification()
    else:
        return handle_incoming_messages()


def handle_verification():
    return request.args['hub.challenge']


def process_payload(sender, payload):
    send_message(sender, "Your button has payload {}".format(payload))


def handle_incoming_messages():
    data = request.json
    messaging_events = data['entry'][0]['messaging']

    for event in messaging_events:
        sender = event['sender']['id']
        if 'message' in event and 'text' in event['message']:
            text = event['message']['text']
            process_message(sender, text)
        elif 'postback' in event and 'payload' in event['postback']:
            payload = event['postback']['payload']
            process_payload(sender, payload)

    return "ok"


def sendpic(sender):
    r = requests.get("https://graph.facebook.com/v2.6/"+sender+"?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" + ACCESS_TOKEN)
    photo = r.json()["profile_pic"]
    data = {
        "recipient": {
            "id": sender
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": photo
                }
            }
        }
    }
    send(data)


def send_button(sender):
    data = {
        "recipient": {
            "id": sender
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "What do you want to do next?",
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "http://google.com/",
                            "title": "Show Website"
                        },
                        {
                            "type": "postback",
                            "title": "I want ...",
                            "payload": "I_WANT"
                        }
                    ]
                }
            }
        }
    }
    send(data)


def send(data):
    return requests.post(
        "https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN,
        json=data)


def greeting(sender):
    r = requests.get("https://graph.facebook.com/v2.6/"+sender+"?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" + ACCESS_TOKEN)
    message = "Hola, " + r.json()["first_name"]
    send_message(sender, message)

if __name__ == '__main__':
    app.run(port=9842, debug=True)
