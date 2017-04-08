from flask import Flask, request
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAAbCANkytUYBAHcOtp4HcKyJfKwdAX1X9NZCjLynZC26u0hSBvoDZAPDOIdmjf8GlcwUSCDn0eQjqfi3undSU6eFfHInckBHCLex8wG5oCsK0iwdOqT0vnKpDKBg0AMy0LOUlEkBGfzoy2iACjczPXBN3QHD0lD1UZB1hyXPygZDZD"


def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg,
        }
    }
    resp = requests.post(
        "https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN,
        json=data)
    print resp.content


def process_message(sender, message):
    greeting(sender)
    sendpic(sender)
    words = message.split()
    reply(sender, "tus palabras fueron: {}".format(words))


@app.route('/', methods=['GET', 'POST'])
def handle_request():
    print request.method
    if request.method == 'GET':
        return handle_verification()
    else:
        return handle_incoming_messages()


def handle_verification():
    return request.args['hub.challenge']


def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    process_message(sender, message)
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
    resp = requests.post(
        "https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN,
        json=data)


def greeting(sender):
    r = requests.get("https://graph.facebook.com/v2.6/"+sender+"?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" + ACCESS_TOKEN)
    message = "Hola, " + r.json()["first_name"]
    reply(sender, message)

if __name__ == '__main__':
    app.run(port=9842, debug=True)
